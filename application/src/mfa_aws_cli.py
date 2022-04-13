#!/usr/bin/env python3
from abc import ABC, abstractmethod
import argparse
import configparser
from dataclasses import dataclass
import os
from typing import Dict, Optional

import boto3
from botocore.exceptions import ClientError, ParamValidationError

AWS_DIR = f"{os.path.expanduser('~')}/.aws"


class UserInputInvalid(Exception):
    pass


class ProfileDoesNotExist(Exception):
    pass


class ProfileManager(configparser.ConfigParser, ABC):
    profile_name: str

    def __init__(self, profile_name: str, verbose: bool = False):
        self.profile_name = profile_name
        self.verbose = verbose
        super().__init__()
        self._read_file()

    @property
    @abstractmethod
    def path(self) -> str:
        """path to this config file"""

    def __enter__(self):
        self._read_file()
        return self

    def __exit__(self, type, value, traceback):
        self.save_file()

    def _read_file(self) -> None:
        super().read(self.path)

    def save_file(self) -> None:
        with open(self.path, 'w') as fout:
            super().write(fout)

    def exists(self) -> bool:
        return self.has_section(self.profile_name)

    def update_profile(self, profile_name: Optional[str] = None, **kwargs):
        profile_name = profile_name or self.profile_name

        if not self.has_section(profile_name):
            self.add_section(profile_name)

        for key, value in kwargs.items():
            self.set(profile_name, key, value)


@dataclass
class UserProfileParameters:
    profile_name: str
    iam_username: str
    account_id: str


class AutoSTSProfileManager(ProfileManager):

    @property
    def path(self) -> str:
        return f"{AWS_DIR}/auto_sts.cfg"

    def __init__(self, profile_name: str, verbose: bool):
        super().__init__(profile_name, verbose)
        if not self.has_section(profile_name):
            self.add_section(profile_name)

        if not self.account_id:
            account_id = input("ID da conta (número de 12 dígitos): ")
            account_id = account_id.replace(' ', '').replace('-', '')
            if not account_id:
                raise UserInputInvalid("\tAccount ID é obrigatório")
            self.account_id = account_id

        if not self.iam_username:
            iam_username = input("Nome do usuário IAM: ")
            if not iam_username:
                raise UserInputInvalid("Usuário IAM é obrigatório")
            self.iam_username = iam_username

    @property
    def account_id(self):
        return self.get(self.profile_name, 'account_id', fallback=None)

    @account_id.setter
    def account_id(self, value):
        self.set(self.profile_name, 'account_id', value)

    @property
    def iam_username(self):
        return self.get(self.profile_name, 'iam_username', fallback=None)

    @iam_username.setter
    def iam_username(self, value):
        self.set(self.profile_name, 'iam_username', value)

    @property
    def mfa_arn(self) -> str:
        return f"arn:aws:iam::{self.account_id}:mfa/{self.iam_username}"


class AWSCredsProfileManager(ProfileManager):
    @property
    def path(self) -> str:
        return f"{AWS_DIR}/credentials"

    @property
    def mfa_name(self) -> str:
        return f"{self.profile_name}_mfa"

    def update_profile(self, **kwargs):
        if not self.has_section(self.mfa_name):
            self.add_section(self.mfa_name)
        return super().update_profile(profile_name=self.mfa_name, **kwargs)


@dataclass
class STSHandler:
    profile: AutoSTSProfileManager
    region: str

    def get_sts_credentials(self, token: Optional[str] = None) -> Dict[str, str]:
        session = boto3.Session(profile_name=self.profile.profile_name, region_name=self.region)
        sts = session.client('sts')
        token = token or input("Token: ")
        while True:
            try:
                response = sts.get_session_token(
                    SerialNumber=self.profile.mfa_arn,
                    TokenCode=token,
                )
                break
            except ParamValidationError as e:
                token = input('Token com formato inválido. Tente novamente: ')
            except ClientError:
                token = input('Erro de autenticação, o token expirou? Tente novamente: ')

        return {
            'aws_access_key_id': response['Credentials']['AccessKeyId'],
            'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
            'aws_session_token': response['Credentials']['SessionToken'],
        }


def main():
    parser = argparse.ArgumentParser(description='Update AWS MFA credentials')
    parser.add_argument('profile', nargs='?', default=None,
                        help='Nome do perfil (como em ~/.aws/credentials)')
    parser.add_argument('token', nargs='?', help='Token MFA', default=None)
    parser.add_argument('--token', '-t', help='Token MFA', default=None)
    parser.add_argument('--region', '-r', help='Região AWS', default='us-east-1')
    parser.add_argument('--verbose', '-v', help='Verbose', action='store_true')

    args = parser.parse_args()
    profile = args.profile
    if profile is None:
        profile = input(f"Nome do perfil (mesmo que em ~/.aws/credentials): ")

    with AWSCredsProfileManager(profile, args.verbose) as aws_creds_profile:
        if not aws_creds_profile.exists():
            print(
                f"Perfil '{profile}' não encontrado. Verifique que o perfil "
                "está em ~/.aws/credentials e tente novamente."
            )
            return

        with AutoSTSProfileManager(profile, args.verbose) as auto_sts_profile:
            sts_handler = STSHandler(auto_sts_profile, args.region)
            creds = sts_handler.get_sts_credentials(args.token)

        if args.verbose:
            print(*[f"{k}: {v}" for k, v in creds.items()], sep='\n')

        aws_creds_profile.update_profile(**creds)
        print(f"Perfil de nome '{aws_creds_profile.mfa_name}' atualizado com sucesso")


if __name__ == "__main__":
    main()
