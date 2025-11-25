import logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

    @property
    def nom(self) -> str:
        return self._nom

    def deposer(self, montant: float):
        if montant <= 0:
            raise MontantNegatifException(f"Le montant du dépôt doit être positif. Reçu : {montant}€")
        self._solde += montant

    def retirer(self, montant: float):
        if montant <= 0:
            raise MontantNegatifException(f"Le montant du retrait doit être positif. Reçu : {montant}€")
        
        if montant > self._solde:
            raise SoldeInsuffisantException("Solde insuffisant pour ce retrait.")

        self._solde -= montant

    def afficher(self):
        print(f"Compte: {self.nom}, Solde: {self.solde:.2f}€")

if __name__ == '__main__':
    try:
        compte = CompteBancaire("Alice", 100)
        compte.afficher()
        compte.deposer(50)
        print(f"Après dépôt: Solde: {compte.solde}€")

    except TransactionException as e:
        logging.error(f"Erreur inattendue: {e}")

    try:
        compte.retirer(150)

    except SoldeInsuffisantException as e:
        print("\nErreur de Retrait (Solde):", e)
        logging.warning(f"Tentative de retrait échouée pour {compte.nom}: {e}")

    try:
        compte.deposer(-10)

    except MontantNegatifException as e:
        print("\nErreur de Dépôt (Montant):", e)

    except TransactionException as e:
        print("\nErreur de Transaction Générique:", e)