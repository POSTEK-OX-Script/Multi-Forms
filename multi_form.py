from ox_script import *
import datetime
import os

form_list = []
selected_form = ""


def find_forms():
    global selected_form
    global form_list
    form_list = [file for file in os.listdir() if file.endswith(".txt")]
    if(len(form_list) != 0):
        selected_form = form_list[0]


def update_selected_form(value):
    global form_list
    global selected_form
    selected_form = form_list[int(value)]


def start_printing():
    global selected_form
    global today_date
    serial_num = int(serial_num_controller.value)
    for i in range(0, int(print_num_controller.value)):
        cmd = PTK_UpdateAllFormVariables(
            selected_form,
            Input1=today_date,
            Input2="{:03d}".format(serial_num + i),
        )
        PTK_SendCmdToPrinter(cmd)


def empty(value):
    pass


if __name__ == "__main__":
    find_forms()
    controller = PTK_UIInit(
        PTK_UIPage(
            form_list_controller := PTK_UIList(
                title="Form Name",
                items=form_list,
                valueType="int",
                value=0,
                Onpressed=update_selected_form,
            ),
            date_controller := PTK_UITextBox(title="Today's Date", value="--"),
            serial_num_controller := PTK_UIInput(
                title="Starting Serial", value="001", Onsubmit=empty
            ),
            print_num_controller := PTK_UIInput(
                title="Print Quantity", value="001", Onsubmit=empty
            ),
            PTK_UIButton(title="Print", Onpressed=start_printing),
        ),
        # Setting require_execute_confirmation to False will allow the script to run without the need to press the execute button on the printer
        require_execute_confirmation=False,
    )
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    date_controller.update(today_date)
