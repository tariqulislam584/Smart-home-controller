import flet as ft
from datetime import datetime


def main(page: ft.Page):
    page.title = "Smart Home Controller"
    page.padding = 20
    page.theme_mode = "light"
    page.window_width = 950
    page.window_height = 700

    # -------------------------
    # DEVICE STATES
    # -------------------------
    light_on = False
    door_locked = True
    thermostat_value = 22
    fan_speed = 0

    # -------------------------
    # UI LABELS TO UPDATE LIVE
    # -------------------------
    light_status = ft.Text()
    door_status = ft.Text()
    thermo_status = ft.Text()
    fan_status = ft.Text()

    # -------------------------
    # LOGS
    # -------------------------
    device_logs = {
        "light": [],
        "door": [],
        "thermostat": [],
        "fan": []
    }

    action_log = []
    power_data = []

    # -------------------------
    # POWER CALCULATION
    # -------------------------
    def calc_power():
        p = 0
        if light_on:
            p += 20
        if not door_locked:
            p += 5
        p += (thermostat_value - 18) * 2
        p += fan_speed * 10
        return p

    def record(device_key, device_id, action):
        current_time = datetime.now().strftime("%H:%M:%S")
        device_logs[device_key].append(f"{current_time} – {action} (User)")

        action_log.append({
            "time": current_time,
            "device": device_id,
            "action": action,
            "user": "User"
        })

        power_data.append({
            "x": len(power_data),
            "y": calc_power()
        })

    # -------------------------
    # ACTIONS
    # -------------------------
    def toggle_light(e):
        nonlocal light_on
        light_on = not light_on
        record("light", "light1", "Turn ON" if light_on else "Turn OFF")

        light_status.value = f"Status: {'ON' if light_on else 'OFF'}"
        e.control.text = "Turn OFF" if light_on else "Turn ON"
        light_status.update()
        e.control.update()

        page.update()

    def toggle_door(e):
        nonlocal door_locked
        door_locked = not door_locked
        record("door", "door1", "Unlock" if not door_locked else "Lock")

        door_status.value = f"Door: {'LOCKED' if door_locked else 'UNLOCKED'}"
        e.control.text = "Unlock" if door_locked else "Lock"
        door_status.update()
        e.control.update()

        page.update()

    def change_temp(e):
        nonlocal thermostat_value
        thermostat_value = int(e.control.value)
        record("thermostat", "thermo1", f"Set {thermostat_value}°C")

        thermo_status.value = f"Set point: {thermostat_value} °C"
        thermo_status.update()
        page.update()

    def change_fan(e):
        nonlocal fan_speed
        fan_speed = int(e.control.value)
        record("fan", "fan1", f"Speed {fan_speed}")

        fan_status.value = f"Fan speed: {fan_speed}"
        fan_status.update()
        page.update()

    # -------------------------
    # HEADER
    # -------------------------
    def header(active):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Smart Home Controller", size=26, weight="bold"),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            "Overview",
                            on_click=lambda e: page.go("/"),
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE if active == "overview" else ft.Colors.BLACK
                            )
                        ),
                        ft.TextButton(
                            "Statistics",
                            on_click=lambda e: page.go("/stats"),
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE if active == "stats" else ft.Colors.BLACK
                            )
                        )
                    ]
                )
            ]
        )

    # -------------------------
    # DETAILS PAGE TEMPLATE
    # -------------------------
    def detail_page(device_key, title, id, type, state):
        return ft.View(
            route=f"/details/{device_key}",
            controls=[
                ft.Text("Smart Home Controller", size=26, weight="bold"),
                ft.Container(
                    width=600,
                    padding=20,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    content=ft.Column(
                        controls=[
                            ft.Text(f"{title} details", size=22, weight="bold"),
                            ft.Text(f"ID: {id}"),
                            ft.Text(f"Type: {type}"),
                            ft.Text(f"State: {state}", weight="bold"),
                            ft.Text("Recent actions", size=20, weight="bold"),
                            ft.Column([ft.Text(t) for t in device_logs[device_key]]),
                            ft.TextButton("Back to overview", on_click=lambda e: page.go("/"))
                        ]
                    )
                )
            ]
        )

    # -------------------------
    # ROUTES
    # -------------------------
    def route_change(route):
        page.views.clear()

        # always sync labels
        light_status.value = f"Status: {'ON' if light_on else 'OFF'}"
        door_status.value = f"Door: {'LOCKED' if door_locked else 'UNLOCKED'}"
        thermo_status.value = f"Set point: {thermostat_value} °C"
        fan_status.value = f"Fan speed: {fan_speed}"

        # -------------------- OVERVIEW -----------------------
        if page.route == "/":
            light_card = ft.Container(
                width=360, bgcolor="#FFEFC2", padding=15, border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text("Living Room Light", size=18, weight="bold"),
                        light_status,
                        ft.Text("Tap to switch the light."),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.TextButton("Details", on_click=lambda e: page.go("/details/light")),
                                ft.FilledButton(
                                    "Turn ON" if not light_on else "Turn OFF",
                                    on_click=toggle_light,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.BLUE,                # Normal background
                                        color=ft.Colors.WHITE,                 # Text color
                                        overlay_color=ft.Colors.LIGHT_BLUE,   # Hover color
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
)                            ]
                        )
                    ]
                )
            )

            door_card = ft.Container(
                width=360, bgcolor="#FBE2D0", padding=15, border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text("Front Door", size=18, weight="bold"),
                        door_status,
                        ft.Text("Tap to lock/unlock the door."),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.TextButton("Details", on_click=lambda e: page.go("/details/door")),
                                ft.FilledButton(
                                    "Unlock" if door_locked else "Lock",
                                    on_click=toggle_door,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.RED,
                                        color=ft.Colors.WHITE,
                                        overlay_color=ft.Colors.PINK,
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
)                            ]
                        )
                    ]
                )
            )

            thermo_card = ft.Container(
                width=360, bgcolor="#FFD6E0", padding=15, border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text("Thermostat", size=18, weight="bold"),
                        thermo_status,
                        ft.Text("Use slider to change temperature."),
                        ft.Slider(min=15, max=30, value=thermostat_value, on_change=change_temp),
                        ft.TextButton("Details", on_click=lambda e: page.go("/details/thermostat"))
                    ]
                )
            )

            fan_card = ft.Container(
                width=360, bgcolor="#D6F5FF", padding=15, border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text("Ceiling Fan", size=18, weight="bold"),
                        fan_status,
                        ft.Text("0 = OFF, 3 = MAX."),
                        ft.Slider(min=0, max=3, divisions=3, value=fan_speed, on_change=change_fan),
                        ft.TextButton("Details", on_click=lambda e: page.go("/details/fan"))
                    ]
                )
            )

            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        header("overview"),
                        ft.Text("On/Off devices", size=20, weight="bold"),
                        ft.Row([light_card, door_card], spacing=20),
                        ft.Text("Slider controlled devices", size=20, weight="bold"),
                        ft.Row([thermo_card, fan_card], spacing=20)
                    ]
                )
            )

        # -------------------- STATISTICS -----------------------
        elif page.route == "/stats":

            if len(power_data) > 0:
                points = [ft.LineChartDataPoint(p["x"], p["y"]) for p in power_data]
                max_x = max((p["x"] for p in power_data), default=10)
                max_y = max((p["y"] for p in power_data), default=10)
            else:
                points = [ft.LineChartDataPoint(0, 0)]
                max_x = 10
                max_y = 10

            chart = ft.LineChart(
                data_series=[ft.LineChartData(points)],
                min_x=0, max_x=max_x, min_y=0, max_y=max_y,
                expand=True,
                border=ft.border.all(1, ft.Colors.GREY_400)
            )

            table = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Time")),
        ft.DataColumn(ft.Text("Device")),
        ft.DataColumn(ft.Text("Action")),
        ft.DataColumn(ft.Text("User")),
    ],
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(log["time"])),
                ft.DataCell(ft.Text(log["device"])),
                ft.DataCell(ft.Text(log["action"])),
                ft.DataCell(ft.Text(log["user"])),
            ],
            color="#FFFFFF" if i % 2 == 0 else "#F3F4F6"  # Alternate row colors
        )
        for i, log in enumerate(action_log)
    ],
    expand=True
)


            page.views.append(
                ft.View(
                    route="/stats",
                    controls=[
                        header("stats"),
                        ft.Text("Power consumption (simulated)", size=20, weight="bold"),
                        ft.Container(height=260, padding=10, bgcolor=ft.Colors.WHITE, content=chart,
                                     border=ft.border.all(1, ft.Colors.GREY_300)),
                        ft.Text("Action log", size=20, weight="bold"),
                        ft.Container(
                        padding=10,
                            bgcolor="#F9FAFB",  # Soft light gray background
                            content=table,
                            border=ft.border.all(1, ft.Colors.GREY_200),
                            border_radius=8,  # Rounded corners for softer look
                            expand=True    
                        )

                    ]
                )
            )

        # -------------------- DETAILS -----------------------
        elif page.route == "/details/light":
            page.views.append(detail_page("light", "Living Room Light", "light1", "light",
                                          "ON" if light_on else "OFF"))

        elif page.route == "/details/door":
            page.views.append(detail_page("door", "Front Door", "door1", "door",
                                          "LOCKED" if door_locked else "UNLOCKED"))

        elif page.route == "/details/thermostat":
            page.views.append(detail_page("thermostat", "Thermostat", "thermo1", "thermostat",
                                          f"{thermostat_value}°C"))

        elif page.route == "/details/fan":
            page.views.append(detail_page("fan", "Ceiling Fan", "fan1", "fan",
                                          f"Speed {fan_speed}"))

        page.update()

    # ROUTER
    page.on_route_change = route_change
    page.go("/")


ft.app(target=main)