__all__ = ["AbstractSMTPRepository"]

from abc import ABCMeta, abstractmethod


class AbstractSMTPRepository(metaclass=ABCMeta):
    @abstractmethod
    def send(self, message: str, to: str):
        """
        Send message to email.

        :param message: message text (formed from :class:`MIMEMultipart`).
        :param to: email address.
        """

    @abstractmethod
    def send_connect_email(self, email: str, auth_code: str):
        """
        Send message to email.

        :param email: email address.
        :param auth_code: auth code.
        """
