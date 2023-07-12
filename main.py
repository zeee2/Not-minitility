import shutil
import string
import win32api
import time
import customtkinter
import urllib.request
from common.config import *
from common.minipad import *


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

VER = "v1.1"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.currentProfile = 1

        self.title("Minipad Utility (v0.2) *unofficial")
        self.geometry(f"{750}x{400}")
        self.resizable(False, False)


        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # 사이드바
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Profile", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.profile_button_1 = customtkinter.CTkButton(self.sidebar_frame, fg_color="#3B8ED0" if self.currentProfile == 1 else "transparent", text="Profile 1", command=self.profile_handler_1)
        self.profile_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.profile_button_2 = customtkinter.CTkButton(self.sidebar_frame, fg_color="#3B8ED0" if self.currentProfile == 2 else "transparent", text="Profile 2", command=self.profile_handler_2)
        self.profile_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.profile_button_3 = customtkinter.CTkButton(self.sidebar_frame, fg_color="#3B8ED0" if self.currentProfile == 3 else "transparent", text="Profile 3", command=self.profile_handler_3)
        self.profile_button_3.grid(row=3, column=0, padx=20, pady=(10, 50))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))


        # 탭 정의
        self.tabview = customtkinter.CTkTabview(self, width=650, height=340)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.tabview.add("설정")
        self.tabview.add("펌웨어")
        self.tabview.tab("설정").grid_columnconfigure(0, weight=1)
        self.tabview.tab("펌웨어").grid_columnconfigure(0, weight=1)

        self.toggle_rapidtrigger = customtkinter.StringVar(value="1")
        self.toggle_continuous_rapidtrigger = customtkinter.StringVar(value="1")
        self.toggle_hid = customtkinter.StringVar(value="1")

        # 설정 탭
        self.tab_setting_actuationpoint_label = customtkinter.CTkLabel(self.tabview.tab("설정"),
                                                                       text=f"입력 지점",
                                                                       font=customtkinter.CTkFont(size=16, weight="bold"))
        self.tab_setting_actuationpoint_label.grid(row=0, column=0, padx=0, pady=(20,0), sticky="nsew")
        self.tab_setting_actuationpoint_value = customtkinter.CTkLabel(self.tabview.tab("설정"),
                                                                       text=f"{(int(controller.MINIPAD_DATA['1']['uh']) - int(controller.MINIPAD_DATA['1']['lh'])) / 100} mm")
        self.tab_setting_actuationpoint_value.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.tab_setting_actuationpoint_slider = customtkinter.CTkSlider(self.tabview.tab("설정"),orientation="vertical",
                                                                         from_=39, to=1, number_of_steps=39, command=self.actuationpoint_change_event)
        self.tab_setting_actuationpoint_slider.grid(row=0, column=1, rowspan=3, padx=0, pady=20, sticky="nsew")

        self.tab_setting_rapidtrigger_label = customtkinter.CTkLabel(self.tabview.tab("설정"),
                                                                       text=f"래피드 트리거",
                                                                       font=customtkinter.CTkFont(size=16, weight="bold"))
        self.tab_setting_rapidtrigger_label.grid(row=0, column=2, padx=30, pady=(20,0), sticky="nsew")
        self.tab_setting_rapidtrigger_value = customtkinter.CTkLabel(self.tabview.tab("설정"),
                                                                       text=f"up: {round(int(controller.MINIPAD_DATA['1']['rtus']) * 0.01, 1)} mm\ndown: {round(int(controller.MINIPAD_DATA['1']['rtds']) * 0.01, 1)} mm")
        self.tab_setting_rapidtrigger_value.grid(row=1, column=2, padx=0, pady=0, sticky="nsew") 
        self.tab_setting_rapidtrigger_slider_up = customtkinter.CTkSlider(self.tabview.tab("설정"), orientation="vertical",
                                                                       from_=20, to=1, number_of_steps=20, command=self.rapidtrigger_change_up_event)
        self.tab_setting_rapidtrigger_slider_up.grid(row=0, column=3, rowspan=3, padx=0, pady=0, sticky="nsew")
        self.tab_setting_rapidtrigger_slider_down = customtkinter.CTkSlider(self.tabview.tab("설정"), orientation="vertical",
                                                                       from_=20, to=1, number_of_steps=20, command=self.rapidtrigger_change_down_event)
        self.tab_setting_rapidtrigger_slider_down.grid(row=0, column=5, rowspan=3, padx=(10, 20), pady=0, sticky="nsew")
    
        self.tab_setting_rapidtrigger_trigger = customtkinter.CTkSwitch(self.tabview.tab("설정"), text="래피드트리거",
                                 variable=self.toggle_rapidtrigger, onvalue="1", offvalue="0", command=self.rapidtrigger_handler)
        self.tab_setting_rapidtrigger_trigger.grid(row=0, column=6, padx=(0, 20), pady=0, sticky="nsew")
        self.tab_setting_continuous_rapidtrigger_trigger = customtkinter.CTkSwitch(self.tabview.tab("설정"), text="지속성 래피드트리거",
                                 variable=self.toggle_continuous_rapidtrigger, onvalue="1", offvalue="0", command=self.continuous_rapidtrigger_handler)
        self.tab_setting_continuous_rapidtrigger_trigger.grid(row=1, column=6, padx=(0, 20), pady=0, sticky="nsew")
        self.tab_setting_comfirm = customtkinter.CTkButton(self.tabview.tab("설정"), text="적용하기",fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.sendAllCmd)
        self.tab_setting_comfirm.grid(row=2, column=6, rowspan=2, padx=0, pady=(20, 20), sticky="nsew")

        
        # 펌웨어 탭
        self.tab_firmware_ver_label = customtkinter.CTkLabel(self.tabview.tab("펌웨어"),
                                                                       text=f"설치된 버전",
                                                                       height=16,
                                                                       font=customtkinter.CTkFont(size=16, weight="bold"))
        self.tab_firmware_ver_label.grid(row=0, column=0, padx=(40,0), pady=(40, 0), sticky="nsw")
        self.tab_firmware_ver_minipad = customtkinter.CTkLabel(self.tabview.tab("펌웨어"),
                                                                       text=f"{controller.MINIPAD_DATA['firmware']}")
        self.tab_firmware_ver_minipad.grid(row=1, column=0, padx=(40,0), pady=0, sticky="nsw")

        self.tab_firmware_ver_latest_label = customtkinter.CTkLabel(self.tabview.tab("펌웨어"),
                                                                       text=f"최신 버전",
                                                                       height=16,
                                                                       font=customtkinter.CTkFont(size=16, weight="bold"))
        self.tab_firmware_ver_latest_label.grid(row=2, column=0, padx=(40,0), pady=0, sticky="nsw")
        self.tab_firmware_ver_latest_minipad = customtkinter.CTkLabel(self.tabview.tab("펌웨어"),
                                                                       text=controller.REPO_DATA["name"])
        self.tab_firmware_ver_latest_minipad.grid(row=3, column=0, padx=(40,0), pady=0, sticky="nsw")

        self.tab_firmware_bootmode = customtkinter.CTkButton(self.tabview.tab("펌웨어"), height=50, text="부트모드 진입",fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.goto_boot_mode)
        self.tab_firmware_bootmode.grid(row=0, column=1, rowspan=2,padx=(0, 40), pady=(40, 10))
        self.tab_firmware_auto_update = customtkinter.CTkButton(self.tabview.tab("펌웨어"), height=50, text="자동 업데이트",fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.firmware_update)
        self.tab_firmware_auto_update.grid(row=2, column=1, rowspan=2, padx=(0, 40), pady=(10, 0))

        self.tab_firmware_calibration = customtkinter.CTkButton(self.tabview.tab("펌웨어"), height=50, text="보정하기",fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.calibrate_handler, state="disabled")
        self.tab_firmware_calibration.grid(row=4, column=0, padx=(40, 0), pady=(20, 0), sticky="nsw")
        self.tab_firmware_hid_toggler = customtkinter.CTkSwitch(self.tabview.tab("펌웨어"), text="키패드 입력 활성화",
                                variable=self.toggle_hid, onvalue="1", offvalue="0", command=self.hid_handler)
        self.tab_firmware_hid_toggler.grid(row=4, column=1, padx=(0, 40), pady=(20, 0))


        self.current_status = customtkinter.CTkLabel(self, text="진행중인 작업이 없습니다.", width=500, height=32)
        self.current_status.grid(row=2, column=1, columnspan=2, padx=20, pady=(0, 20), sticky="nesw")


        self.appearance_mode_optionemenu.set("Dark")

        # 값 불러오기
        self.profile_button_1.configure(fg_color="#3B8ED0" if ProfileManager.config["Current"] == "1" else "transparent")
        self.profile_button_2.configure(fg_color="#3B8ED0" if ProfileManager.config["Current"] == "2" else "transparent")
        self.profile_button_3.configure(fg_color="#3B8ED0" if ProfileManager.config["Current"] == "3" else "transparent")
        self.tab_setting_actuationpoint_slider.set(int(self.calculate_x(int(controller.MINIPAD_DATA['1']['uh']), int(controller.MINIPAD_DATA['1']['lh'])) * 10))
        self.tab_setting_actuationpoint_value.configure(text = f"{round(self.calculate_x(int(controller.MINIPAD_DATA['1']['uh']), int(controller.MINIPAD_DATA['1']['lh'])), 1)} mm")
        self.tab_setting_rapidtrigger_slider_up.set(round(int(controller.MINIPAD_DATA['1']['rtus']) * 0.01, 1) * 10)
        self.tab_setting_rapidtrigger_slider_down.set(round(int(controller.MINIPAD_DATA['1']['rtds']) * 0.01, 1) * 10)
        self.tab_setting_rapidtrigger_value.configure(text = f"up: {round(int(controller.MINIPAD_DATA['1']['rtus']) / 100, 1)} mm\ndown: {round(int(controller.MINIPAD_DATA['1']['rtds']) / 100, 1)} mm")
        if controller.MINIPAD_DATA['1']['rt'] == "0":
            self.tab_setting_rapidtrigger_trigger.deselect()
        else:
            self.tab_setting_rapidtrigger_trigger.select()
        if controller.MINIPAD_DATA['1']['crt'] == "0":
            self.tab_setting_continuous_rapidtrigger_trigger.deselect()
        else:
            self.tab_setting_continuous_rapidtrigger_trigger.select()
        if bool(int(controller.MINIPAD_DATA['1']['hid'])):
            self.tab_firmware_hid_toggler.select()
        else:
            self.tab_firmware_hid_toggler.deselect()

    def calculate_x(self, a_val, b_val):
        x = 0.1 + 0.1 * ((a_val - 390) / -10)
        return x
    
    def refresh_ui(self):
        # 값 변경
        self.tab_setting_actuationpoint_slider.set(int(self.calculate_x(int(controller.MINIPAD_DATA['1']['uh']), int(controller.MINIPAD_DATA['1']['lh'])) * 10))
        self.tab_setting_actuationpoint_value.configure(text = f"{round(self.calculate_x(int(controller.MINIPAD_DATA['1']['uh']), int(controller.MINIPAD_DATA['1']['lh'])), 1)} mm")
        self.tab_setting_rapidtrigger_slider_up.set(round(int(controller.MINIPAD_DATA['1']['rtus']) * 0.01, 1) * 10)
        self.tab_setting_rapidtrigger_slider_down.set(round(int(controller.MINIPAD_DATA['1']['rtds']) * 0.01, 1) * 10)
        self.tab_setting_rapidtrigger_value.configure(text = f"up: {round(int(controller.MINIPAD_DATA['1']['rtus']) / 100, 1)} mm\ndown: {round(int(controller.MINIPAD_DATA['1']['rtds']) / 100, 1)} mm")
        if controller.MINIPAD_DATA['1']['rt'] == "0":
            self.tab_setting_rapidtrigger_trigger.deselect()
        else:
            self.tab_setting_rapidtrigger_trigger.select()
        if controller.MINIPAD_DATA['1']['crt'] == "0":
            self.tab_setting_continuous_rapidtrigger_trigger.deselect()
        else:
            self.tab_setting_continuous_rapidtrigger_trigger.select()
        if bool(int(controller.MINIPAD_DATA['1']['hid'])):
            self.tab_firmware_hid_toggler.select()
        else:
            self.tab_firmware_hid_toggler.deselect()

    def profile_change_after(self):
        # 명령 대기열에 프로필 변경값 저장
        for profile in ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]:
            controller.MINIPAD_DATA["1"][profile] = ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"][profile]
            controller.MINIPAD_DATA["2"][profile] = ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"][profile]
            controller.MINIPAD_DATA["3"][profile] = ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"][profile]
            if not profile in controller.CMD_LIST:
                controller.CMD_LIST.append(profile)
        if int(controller.MINIPAD_DATA["1"]["lh"]) > int(controller.MINIPAD_DATA["1"]["uh"]):
            controller.MINIPAD_DATA["1"][controller.MINIPAD_DATA["1"].index("lh")], controller.MINIPAD_DATA["1"][controller.MINIPAD_DATA["1"].index("uh")] = controller.MINIPAD_DATA["1"][controller.MINIPAD_DATA["1"].index("lh")]

        # 값 변경
        self.tab_setting_actuationpoint_slider.set(int(self.calculate_x(int(controller.MINIPAD_DATA['1']['uh']), int(controller.MINIPAD_DATA['1']['lh'])) * 10))
        self.tab_setting_actuationpoint_value.configure(text = f"{round(self.calculate_x(int(controller.MINIPAD_DATA['1']['uh']), int(controller.MINIPAD_DATA['1']['lh'])), 1)} mm")
        self.tab_setting_rapidtrigger_slider_up.set(round(int(controller.MINIPAD_DATA['1']['rtus']) * 0.01, 1) * 10)
        self.tab_setting_rapidtrigger_slider_down.set(round(int(controller.MINIPAD_DATA['1']['rtds']) * 0.01, 1) * 10)
        self.tab_setting_rapidtrigger_value.configure(text = f"up: {round(int(controller.MINIPAD_DATA['1']['rtus']) / 100, 1)} mm\ndown: {round(int(controller.MINIPAD_DATA['1']['rtds']) / 100, 1)} mm")
        if ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]['rt'] == "0":
            self.tab_setting_rapidtrigger_trigger.deselect()
        else:
            self.tab_setting_rapidtrigger_trigger.select()
        if ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]['crt'] == "0":
            self.tab_setting_continuous_rapidtrigger_trigger.deselect()
        else:
            self.tab_setting_continuous_rapidtrigger_trigger.select()
        if bool(int(controller.MINIPAD_DATA['1']['hid'])):
            self.tab_firmware_hid_toggler.deselect()
        else:
            self.tab_firmware_hid_toggler.select()

    def profile_handler_1(self):
        self.profile_button_1.configure(fg_color="#3B8ED0")
        self.profile_button_2.configure(fg_color="transparent")
        self.profile_button_3.configure(fg_color="transparent")

        ProfileManager.config["Current"] = "1"
        ProfileManager.save_config()

        self.profile_change_after()

    def profile_handler_2(self):
        self.profile_button_2.configure(fg_color="#3B8ED0")
        self.profile_button_1.configure(fg_color="transparent")
        self.profile_button_3.configure(fg_color="transparent")

        ProfileManager.config["Current"] = "2"
        ProfileManager.save_config()

        self.profile_change_after()

    def profile_handler_3(self):
        self.profile_button_3.configure(fg_color="#3B8ED0")
        self.profile_button_1.configure(fg_color="transparent")
        self.profile_button_2.configure(fg_color="transparent")

        ProfileManager.config["Current"] = "3"
        ProfileManager.save_config()

        self.profile_change_after()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def update_current_status(self):
        self.current_status.configure(text=f"{len(controller.CMD_LIST)}개의 작업 대기중... '적용하기'를 누르면 작업이 진행됩니다.")

    def sendAllCmd(self, change_status=True):
        if len(controller.CMD_LIST) <= 0:
            return
        disabled = [self.profile_button_1, self.profile_button_2, self.profile_button_3, self.tab_setting_comfirm]
        for ele in disabled:
            ele.configure(state="disabled")
        
        commands = []

        for cmd in controller.CMD_LIST:
            commands.append(f"hkey.{cmd} {controller.MINIPAD_DATA['1'][cmd]}")
        commands.append("save")
        
        if change_status:
            self.current_status.configure(text=f"{len(controller.CMD_LIST)}개의 작업 진행중...")
            controller.multiple_send_command(commands, self.current_status, [self.profile_button_1, self.profile_button_2, self.profile_button_3, self.tab_setting_comfirm])
        else:
            controller.multiple_send_command(commands)

        controller.CMD_LIST = []

        ProfileManager.save_config()

    def actuationpoint_change_event(self, val):
        def calculate_value(x):
            uh = int(390 - 10 * ((x - 0.1) / 0.1))
            lh = int(380 - 10 * ((x - 0.1) / 0.1))
            return uh, lh
        
        value = round(val / 10, 1)
        self.tab_setting_actuationpoint_value.configure(text = f"{value} mm")
        NEW_UH, NEW_LH = calculate_value(value)

        if controller.MINIPAD_DATA["1"]["lh"] != NEW_LH:
            if not "lh" in controller.CMD_LIST and not "uh" in controller.CMD_LIST:
                if NEW_LH >= int(controller.MINIPAD_DATA["1"]["uh"]):
                    controller.CMD_LIST.append("uh")
                    controller.CMD_LIST.append("lh")
                else:
                    controller.CMD_LIST.append("lh")
                    controller.CMD_LIST.append("uh")

            controller.MINIPAD_DATA["1"]["uh"] = NEW_UH
            controller.MINIPAD_DATA["2"]["uh"] = NEW_UH
            controller.MINIPAD_DATA["3"]["uh"] = NEW_UH
            controller.MINIPAD_DATA["1"]["lh"] = NEW_LH
            controller.MINIPAD_DATA["2"]["lh"] = NEW_LH
            controller.MINIPAD_DATA["3"]["lh"] = NEW_LH

            ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]["uh"] = str(NEW_UH)
            ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]["lh"] = str(NEW_LH)

            self.update_current_status()

    def rapidtrigger_change_up_event(self, val):
        value = round(val / 10, 1)
        NEW_VALUE = int(value * 100)

        if controller.MINIPAD_DATA["1"]["rtus"] != NEW_VALUE:
            if not "rtus" in controller.CMD_LIST:
                controller.CMD_LIST.append("rtus")

            controller.MINIPAD_DATA["1"]["rtus"] = NEW_VALUE
            controller.MINIPAD_DATA["2"]["rtus"] = NEW_VALUE
            controller.MINIPAD_DATA["3"]["rtus"] = NEW_VALUE

            ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]['rtus'] = str(NEW_VALUE)

        self.tab_setting_rapidtrigger_value.configure(text = f"up: {value} mm\ndown: {round((int(controller.MINIPAD_DATA['1']['rtds']) / 100), 1)} mm")

        self.update_current_status()

    def rapidtrigger_change_down_event(self, val):
        value = round(val / 10, 1)
        NEW_VALUE = int(value * 100)

        if controller.MINIPAD_DATA["1"]["rtds"] != NEW_VALUE:
            if not "rtds" in controller.CMD_LIST:
                controller.CMD_LIST.append("rtds")

            controller.MINIPAD_DATA["1"]["rtds"] = NEW_VALUE
            controller.MINIPAD_DATA["2"]["rtds"] = NEW_VALUE
            controller.MINIPAD_DATA["3"]["rtds"] = NEW_VALUE

            ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]['rtds'] = str(NEW_VALUE)
            
        self.tab_setting_rapidtrigger_value.configure(text = f"up: {round((int(controller.MINIPAD_DATA['1']['rtus']) / 100), 1)} mm\ndown: {value} mm")

        self.update_current_status()

    def rapidtrigger_handler(self):
        VAL = self.toggle_rapidtrigger.get()    

        if VAL == "0":
            if not "crt" in controller.CMD_LIST:
                controller.CMD_LIST.append("crt")

            self.tab_setting_continuous_rapidtrigger_trigger.deselect()
            self.tab_setting_continuous_rapidtrigger_trigger.configure(state="disabled")
            
            controller.MINIPAD_DATA["1"]["crt"] = str(VAL)
            controller.MINIPAD_DATA["2"]["crt"] = str(VAL)
            controller.MINIPAD_DATA["3"]["crt"] = str(VAL)
        else:
            self.tab_setting_continuous_rapidtrigger_trigger.configure(state="normal")
            
        if not "rt" in controller.CMD_LIST:
            controller.CMD_LIST.append("rt")
            
        controller.MINIPAD_DATA["1"]["rt"] = str(VAL)
        controller.MINIPAD_DATA["2"]["rt"] = str(VAL)
        controller.MINIPAD_DATA["3"]["rt"] = str(VAL)

        ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]["rt"] = str(VAL)

        self.update_current_status()

    def continuous_rapidtrigger_handler(self):
        VAL = self.toggle_continuous_rapidtrigger.get() 

        if not "crt" in controller.CMD_LIST:
            controller.CMD_LIST.append("crt")
            
        controller.MINIPAD_DATA["1"]["crt"] = str(VAL)
        controller.MINIPAD_DATA["2"]["crt"] = str(VAL)
        controller.MINIPAD_DATA["3"]["crt"] = str(VAL)

        ProfileManager.config[f"Profile_{ProfileManager.config['Current']}"]["crt"] = str(VAL)

        self.update_current_status()

    def goto_boot_mode(self):
        controller.send_command("boot")
    
    def firmware_update(self):
        self.current_status.configure(text="펌웨어 업데이트 작업 진행중...")

        time.sleep(1)

        print("enter boot mode...")
        controller.send_command("boot")
        
        print("download firmware...")
        url = f"https://github.com/minipadKB/minipad-firmware/releases/download/{controller.REPO_DATA['name']}/minipad_firmware_3k_{controller.REPO_DATA['name']}.uf2"
        file_name = "firmware.uf2"
        minipad_root = ""
        path = ""

        urllib.request.urlretrieve(url, file_name)

        time.sleep(5)

        print("find minipad device...")
        for drive_letter in string.ascii_uppercase:
            drive = drive_letter + ':'
            try:
                volume_info = win32api.GetVolumeInformation(drive)
                free_bytes = win32api.GetDiskFreeSpace(drive)[0]
                if free_bytes <= 128 * 1024 * 1024 and volume_info[0] == "RPI-RP2":
                    minipad_root = drive
                    path = minipad_root + "/" + file_name
            except:
                continue
        
        print("move new firmware... ->", path)
        shutil.move(file_name, path)

        time.sleep(5)

        print("setting start...")
        controller.MINIPAD = controller.connect_minipad()
        
        controller.multiple_send_command(
            ["hkey.rt true", 
             "hkey.crt true",
             "hkey.rtus 10", "hkey.rtds 10",
             "hkey.uh 390", "hkey.lh 380", 
             "hkey1.char 122", "hkey2.char 120", "hkey3.char 99", 
             "hkey.hid true",
             "save"])
        
        controller.thread.join()
        
        controller.get_minipad_data()
        print("reload value")

        self.refresh_ui()
        print('refresh ui')

        self.current_status.configure(text="진행중인 작업이 없습니다.")
        
    def calibrate_handler(self):
        self.current_status.configure(text="보정 작업 초기화 진행중...")
        controller.MINIPAD_DATA["1"]["rest"] = "4095"
        controller.MINIPAD_DATA["1"]["down"] = "0"

        controller.CMD_LIST.append("rest")
        controller.CMD_LIST.append("down")

        self.sendAllCmd(False)

        

    def hid_handler(self):
        controller.CMD_LIST.append("hid")

        controller.MINIPAD_DATA["1"]["hid"] = self.toggle_hid.get()
        controller.MINIPAD_DATA["2"]["hid"] = self.toggle_hid.get()
        controller.MINIPAD_DATA["3"]["hid"] = self.toggle_hid.get()

        self.sendAllCmd()


if __name__ == "__main__":
    controller = MinipadController()

    controller.DEVMODE = True

    controller.get_minipad_data()
    controller.get_minipad_repo_data()

    ProfileManager = ConfigManager()
    ProfileManager.load_config()

    app = App()

    if not re.match(controller.FIRMWARE_PATTERN, controller.MINIPAD_DATA["firmware"]):
        print("firmware detect failed")
        app.firmware_update()
    else:
        print(f"firmware detected: {controller.MINIPAD_DATA['firmware']}")
        

    # if not controller.get_latest_firmware() == VER:


    app.mainloop()