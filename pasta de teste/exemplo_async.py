import asyncio

import PySimpleGUI as sg

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

form = sg.FlexForm(
    "Everything bagel", auto_size_text=True, default_element_size=(40, 1)
)

layout = [
    [
        sg.Text(
            "All graphic widgets in one form!",
            size=(30, 1),
            font=("Helvetica", 25),
            text_color="blue",
        )
    ],
    [sg.Text("Here is some text.... and a place to enter text")],
    [sg.InputText()],
    [
        sg.Checkbox("My first checkbox!"),
        sg.Checkbox("My second checkbox!", default=True),
    ],
    [
        sg.Radio("My first Radio!     ", "RADIO1", default=True),
        sg.Radio("My second Radio!", "RADIO1"),
    ],
    [
        sg.Multiline(
            default_text="This is the default Text shoulsd you decide not to type anything"
        )
    ],
    [
        sg.InputCombo(["Combobox 1", "Combobox 2"], size=(20, 3)),
        sg.Slider(
            range=(1, 100),
            orientation="h",
            size=(35, 20),
            default_value=85,
        ),
    ],
    [
        sg.Listbox(
            values=["Listbox 1", "Listbox 2", "Listbox 3"], size=(30, 6)
        ),
        sg.Slider(
            range=(1, 100),
            orientation="v",
            size=(10, 20),
            default_value=25,
        ),
        sg.Slider(
            range=(1, 100),
            orientation="v",
            size=(10, 20),
            default_value=75,
        ),
        sg.Slider(
            range=(1, 100),
            orientation="v",
            size=(10, 20),
            default_value=10,
        ),
    ],
    [sg.Text("_" * 100, size=(70, 1))],
    [sg.Text("Choose Source and Destination Folders", size=(35, 1))],
    [
        sg.Text(
            "Source Folder",
            size=(15, 1),
            auto_size_text=False,
            justification="right",
        ),
        sg.InputText("Source"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text(
            "Destination Folder",
            size=(15, 1),
            auto_size_text=False,
            justification="right",
        ),
        sg.InputText("Dest"),
        sg.FolderBrowse(),
    ],
    [
        sg.Submit(),
        sg.Cancel(),
        sg.SimpleButton("Customized", button_color=("white", "green")),
    ],
]


form2 = sg.FlexForm(
    "Everything bagel", auto_size_text=True, default_element_size=(40, 1)
)
layout2 = [
    [
        sg.Text(
            "All graphic widgets in one form!",
            size=(30, 1),
            font=("Helvetica", 25),
            text_color="blue",
        )
    ],
    [sg.Text("Here is some text.... and a place to enter text")],
    [sg.InputText()],
    [
        sg.Checkbox("My first checkbox!"),
        sg.Checkbox("My second checkbox!", default=True),
    ],
    [
        sg.Radio("My first Radio!     ", "RADIO1", default=True),
        sg.Radio("My second Radio!", "RADIO1"),
    ],
    [
        sg.Multiline(
            default_text="This is the default Text shoulsd you decide not to type anything"
        )
    ],
    [
        sg.InputCombo(["Combobox 1", "Combobox 2"], size=(20, 3)),
        sg.Slider(
            range=(1, 100),
            orientation="h",
            size=(35, 20),
            default_value=85,
        ),
    ],
    [
        sg.Listbox(
            values=["Listbox 1", "Listbox 2", "Listbox 3"], size=(30, 6)
        ),
        sg.Slider(
            range=(1, 100),
            orientation="v",
            size=(10, 20),
            default_value=25,
        ),
        sg.Slider(
            range=(1, 100),
            orientation="v",
            size=(10, 20),
            default_value=75,
        ),
        sg.Slider(
            range=(1, 100),
            orientation="v",
            size=(10, 20),
            default_value=10,
        ),
    ],
    [sg.Text("_" * 100, size=(70, 1))],
    [sg.Text("Choose Source and Destination Folders", size=(35, 1))],
    [
        sg.Text(
            "Source Folder",
            size=(15, 1),
            auto_size_text=False,
            justification="right",
        ),
        sg.InputText("Source"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text(
            "Destination Folder",
            size=(15, 1),
            auto_size_text=False,
            justification="right",
        ),
        sg.InputText("Dest"),
        sg.FolderBrowse(),
    ],
    [
        sg.Submit(),
        sg.Cancel(),
        sg.SimpleButton("Customized", button_color=("white", "green")),
    ],
]


WINDOWS = set()


async def gui_window_loop():
    main = form.Layout(layout)
    WINDOWS.add(main)
    while True:
        await asyncio.sleep(0.01)
        event, value = main.read(0)
        if event == "__TIMEOUT__":
            continue
        if event == "Exit" or event == None:
            break
        print(event, value)
    main.close()


async def gui_window_loop2():
    main = form2.Layout(layout2)
    WINDOWS.add(main)
    while True:
        await asyncio.sleep(0.01)
        event, value = main.read(0)
        if event == "__TIMEOUT__":
            continue
        if event == "Exit" or event == None:
            break
        print(event, value)
    main.close()


async def auto_close_no_window():
    while True:
        for window in WINDOWS:
            if window.TKrootDestroyed:
                WINDOWS.remove(window)
                break
        await asyncio.sleep(0)
        if len(WINDOWS) == 0:
            return


try:
    window_main = asyncio.ensure_future(gui_window_loop())
    window_main2 = asyncio.ensure_future(gui_window_loop2())

    window_watcher = asyncio.ensure_future(auto_close_no_window())
    window_watcher.add_done_callback(
        lambda f: (print("done_callback callled !"), loop.stop())
    )

    loop.run_forever()

except:

    canceltasks = [task.cancel() for task in asyncio.all_tasks()]

    try:

        print(f"cancelling {len(canceltasks)} tasks")

        loop.run_until_complete(asyncio.wait(canceltasks, timeout=10))

    except asyncio.TimeoutError:

        print("timeout when trying to cancel running tasks")

finally:

    print("closing loop")

    loop.close()