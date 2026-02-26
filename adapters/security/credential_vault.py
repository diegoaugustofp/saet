"""Cofre de credenciais com criptografia Fernet.
Responsavel por armazenar credenciais MT5 de forma protegida (SYS-NFR-020).
"""
import structlog
from cryptography.fernet import Fernet

logger = structlog.get_logger()

class CredentialVault:
    """Cofre para armazenamento seguro de credenciais.
    Usa criptografia simetrica Fernet para proteger senhas
    de contas MT5 conforme SYS-NFR-020.
    """
    
    def __init__(self, encryption_key: str | None = None) -> None:
        """Inicializa o vault com uma chave de criptografia.
        Args:
            encryption_key: Chave Fernet em formato string.
                Se None, gera uma nova chave.
        """
        
        if encryption_key:
            self._fernet = Fernet(encryption_key.encode())
        else:
            key = Fernet.generate_key()
            self._fernet = Fernet(key)
            logger.warning(
                "credential_vault_new_key_generated",
                message="Nova chave de criptografia gerada. "
                "Salve-a em local seguro para persistencia.",
            )
    
    @staticmethod
    def generate_key() -> str:
        """Gera uma nova chave de criptografia Fernet.
        Returns:
            Chave em formato string base64.
        """
        return Fernet.generate_key().decode()
   
    def encrypt(self, plaintext: str) -> str:
        """Criptografa um texto.
        Args:
            plaintext: Texto a ser criptografado.
        Returns:
            Texto criptografado em formato string.
        """
        encrypted = self._fernet.encrypt(plaintext.encode())
        return encrypted.decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Descriptografa um texto.
        Args:
            ciphertext: Texto criptografado.
        Returns:
            Texto original descriptografado.
        """
        decrypted = self._fernet.decrypt(ciphertext.encode())
        return decrypted.decode()