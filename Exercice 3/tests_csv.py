import unittest
import os
from csv_reader import (
    charger_csv, 
    FichierIntrouvableException, 
    LigneInvalideException, 
    PrixNegatifException
)

class TestCsvImport(unittest.TestCase):
    
    def setUp(self):
        self.files_to_remove = []

    def tearDown(self):
        for f in self.files_to_remove:
            if os.path.exists(f):
                os.remove(f)

    def create_temp_csv(self, filename, content):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        self.files_to_remove.append(filename)
        return filename

    def test_import_nominal(self):
        content = "1;Test1;10.5\n2;Test2;20.0"
        filename = self.create_temp_csv("test_nominal.csv", content)
        
        resultat = charger_csv(filename)
        
        self.assertEqual(len(resultat), 2)
        self.assertEqual(resultat[0].nom, "Test1")
        self.assertEqual(resultat[0].prix, 10.5)

    def test_fichier_introuvable(self):
        with self.assertRaises(FichierIntrouvableException):
            charger_csv("fichier_imaginaire_999.csv")

    def test_structure_invalide(self):
        content = "1;Produit;10;EXTRA" 
        filename = self.create_temp_csv("test_structure.csv", content)
        
        with self.assertRaises(LigneInvalideException):
            charger_csv(filename)

    def test_prix_non_numerique(self):
        content = "1;Produit;Douze"
        filename = self.create_temp_csv("test_nan.csv", content)
        
        with self.assertRaises(LigneInvalideException):
            charger_csv(filename)

    def test_prix_negatif(self):
        content = "1;Produit;-5.0"
        filename = self.create_temp_csv("test_negatif.csv", content)
        
        with self.assertRaises(PrixNegatifException):
            charger_csv(filename)

    def test_lignes_vides_ignorees(self):
        content = "1;A;10\n\n\n2;B;20"
        filename = self.create_temp_csv("test_vide.csv", content)
        
        resultat = charger_csv(filename)
        self.assertEqual(len(resultat), 2)

if __name__ == '__main__':
    unittest.main()