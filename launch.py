import sys

import lib.UI.window_init_settings as window
import lib.save_util as save_util

if __name__ == "__main__":

    #create window
    app = window.SettingScreen()

    #load save file
    data_mgr = save_util.SaveLoad()
    data_mgr.Load()

    #send loaded data to necessary places
    app.change_appearance_mode_event(data_mgr.save_file.SavedWindowSettings.Appearance_Theme)

    #run app
    app.mainloop()

    #TODO: need a way to save data
