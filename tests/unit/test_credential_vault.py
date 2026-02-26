"""Testes unitarios para o cofre de credenciais."""

from saet.adapters.security.credential_vault import CredentialVault


class TestCredentialVault:

    def test_generate_key(self) -> None:
        key = CredentialVault.generate_key()
        assert isinstance(key, str)
        assert len(key) > 0

    def test_encrypt_decrypt(self) -> None:
        key = CredentialVault.generate_key()
        vault = CredentialVault(encryption_key=key)

        plaintext = "minha_senha_secreta_123"
        encrypted = vault.encrypt(plaintext)

        assert encrypted != plaintext
        assert vault.decrypt(encrypted) == plaintext

    def test_different_encryptions_same_plaintext(self) -> None:
        key = CredentialVault.generate_key()
        vault = CredentialVault(encryption_key=key)

        plaintext = "test_password"
        encrypted1 = vault.encrypt(plaintext)
        encrypted2 = vault.encrypt(plaintext)

        # Fernet gera tokens diferentes para o mesmo plaintext (por causa do timestamp)
        assert encrypted1 != encrypted2

        # Mas ambos descriptografam para o mesmo valor
        assert vault.decrypt(encrypted1) == plaintext
        assert vault.decrypt(encrypted2) == plaintext

    def test_vault_without_key_generates_new(self) -> None:
        vault = CredentialVault()
        plaintext = "test"
        encrypted = vault.encrypt(plaintext)
        assert vault.decrypt(encrypted) == plaintext