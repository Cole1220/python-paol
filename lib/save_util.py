from dataclasses import dataclass
import pickle

@dataclass
class WindowSettings:
    Appearance_Theme: str = "Dark"

@dataclass
class SaveFile:
    SavedWindowSettings: WindowSettings

class SaveLoad():
    filename = "testSaveFile.pkl"
    save_file = SaveFile(WindowSettings("Dark"))

    def __init__(self):
        super().__init__()

    def Load(self):
        with open(self.filename, 'rb') as file:
            self.save_file = pickle.load(file)

    def Save(self):
        #self.EditSave_Test() #only for testing

        with open(self.filename, 'wb') as file:
            pickle.dump(self.save_file, file)

    def EditSave_Test(self):
        self.save_file.SavedWindowSettings.Appearance_Theme = "Light"