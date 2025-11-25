import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionException(Exception):
    pass

class SoldeInsuffisantException(TransactionException):
    pass

class MontantNegatifException(TransactionException):
    pass

class CompteBancaire:
    def __init__(self, nom: str, solde_initial: float = 0.0):
        self._nom = nom
        self._solde = solde_initial

    @property
    def solde(self) -> float:
        return self._solde

    def deposer(self, montant: float):
        if montant <= 0:
            raise MontantNegatifException(f"Dépôt invalide: {montant}€")
        self._solde += montant

    def retirer(self, montant: float):
        if montant <= 0:
            raise MontantNegatifException(f"Retrait invalide: {montant}€")

        if montant > self._solde:
            raise SoldeInsuffisantException("Solde insuffisant pour ce retrait.")

        self._solde -= montant

if __name__ == "__main__":
    try:
        compte = CompteBancaire("Alice", 100)
        compte.retirer(200)
    except SoldeInsuffisantException as e:
        logging.error(f"Échec transaction: {e}")
    except TransactionException as e:
        print(f"Erreur générique: {e}")