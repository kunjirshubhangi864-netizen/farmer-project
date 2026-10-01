from nicegui import ui


# =========================================================
# FARMER DATA
# =========================================================

farmer_data = {
    "name": "",
    "mobile": "",
    "location": "",
    "season": "",
    "rainfall": "",
    "soil": "",
    "water": ""
}


# =========================================================
# CROP DATABASE
# =========================================================

crop_database = {

    "जास्त": {
        "पावसाळा": [
            "सोयाबीन",
            "मका",
            "तूर",
            "उडीद",
            "मूग",
            "ऊस"
        ],
        "उन्हाळा": [
            "मका",
            "भुईमूग",
            "भाजीपाला",
            "कांदा"
        ],
        "हिवाळा": [
            "गहू",
            "हरभरा",
            "कांदा",
            "ज्वारी"
        ]
    },

    "मध्यम": {
        "पावसाळा": [
            "सोयाबीन",
            "मका",
            "कापूस",
            "तूर",
            "मूग",
            "उडीद"
        ],
        "उन्हाळा": [
            "भुईमूग",
            "मका",
            "कांदा",
            "भाजीपाला"
        ],
        "हिवाळा": [
            "गहू",
            "हरभरा",
            "ज्वारी",
            "कांदा"
        ]
    },

    "कमी": {
        "पावसाळा": [
            "बाजरी",
            "ज्वारी",
            "तूर",
            "हरभरा",
            "मूग",
            "उडीद"
        ],
        "उन्हाळा": [
            "बाजरी",
            "ज्वारी",
            "भुईमूग"
        ],
        "हिवाळा": [
            "हरभरा",
            "ज्वारी",
            "गहू",
            "कांदा"
        ]
    }
}


# =========================================================
# STEP FUNCTIONS
# =========================================================

def show_step(number):

    for step in steps:
        step.set_visibility(False)

    steps[number - 1].set_visibility(True)


def next_name():

    if not name.value:
        ui.notify(
            "कृपया तुमचे नाव टाका",
            type="warning"
        )
        return

    farmer_data["name"] = name.value
    show_step(2)


def next_mobile():

    if not mobile.value:
        ui.notify(
            "कृपया मोबाईल नंबर टाका",
            type="warning"
        )
        return

    farmer_data["mobile"] = mobile.value
    show_step(3)


def next_location():

    if not location.value:
        ui.notify(
            "कृपया गाव किंवा ठिकाण टाका",
            type="warning"
        )
        return

    farmer_data["location"] = location.value
    show_step(4)


def next_season():

    farmer_data["season"] = season.value
    show_step(5)


def next_rain():

    farmer_data["rainfall"] = rainfall.value
    show_step(6)


def next_soil():

    farmer_data["soil"] = soil.value
    show_step(7)


# =========================================================
# SAVE INFORMATION
# =========================================================

def finish_farmer():

    farmer_data["water"] = water.value

    farmer_information.text = (
        "✅ माहिती जतन झाली!\n\n"
        f"👤 नाव: {farmer_data['name']}\n"
        f"📱 मोबाईल: {farmer_data['mobile']}\n"
        f"📍 ठिकाण: {farmer_data['location']}\n"
        f"☀️ हंगाम: {farmer_data['season']}\n"
        f"🌧️ पाऊस: {farmer_data['rainfall']}\n"
        f"🪨 जमीन: {farmer_data['soil']}\n"
        f"💧 पाणी: {farmer_data['water']}"
    )

    information_card.set_visibility(True)
    crop_button.set_visibility(True)

    ui.notify(
        "शेतकऱ्याची माहिती जतन झाली!",
        type="positive"
    )


# =========================================================
# CROP RECOMMENDATION
# =========================================================

def recommend_crops():

    rain = farmer_data["rainfall"]
    season_value = farmer_data["season"]

    crops = crop_database.get(
        rain,
        {}
    ).get(
        season_value,
        []
    )

    # जमिनीप्रमाणे अतिरिक्त पिके

    if farmer_data["soil"] == "कोरडवाहू":

        crops += [
            "बाजरी",
            "ज्वारी",
            "तूर",
            "हरभरा"
        ]

    elif farmer_data["soil"] == "काळी माती":

        crops += [
            "कापूस",
            "सोयाबीन",
            "तूर",
            "ज्वारी"
        ]

    elif farmer_data["soil"] == "मध्यम":

        crops += [
            "सोयाबीन",
            "मका",
            "तूर",
            "हरभरा"
        ]

    elif farmer_data["soil"] == "हलकी":

        crops += [
            "बाजरी",
            "ज्वारी",
            "भुईमूग"
        ]

    # पाण्याप्रमाणे अतिरिक्त पिके

    if farmer_data["water"] == "कमी":

        crops += [
            "बाजरी",
            "ज्वारी",
            "तूर"
        ]

    elif farmer_data["water"] == "जास्त":

        crops += [
            "मका",
            "ऊस",
            "भाजीपाला"
        ]

    # Duplicate काढणे

    crops = list(dict.fromkeys(crops))

    crops = crops[:8]

    crop_result.text = (
        "🌱 तुमच्या शेतासाठी पिकांची शिफारस\n\n"
        f"📍 ठिकाण: {farmer_data['location']}\n"
        f"🌧️ पाऊस: {farmer_data['rainfall']}\n"
        f"☀️ हंगाम: {farmer_data['season']}\n"
        f"🪨 जमीन: {farmer_data['soil']}\n"
        f"💧 पाणी: {farmer_data['water']}\n\n"
        "🌾 सुचवलेली पिके:\n\n"
        +
        "\n".join(
            [
                f"🌱 {i + 1}. {crop}"
                for i, crop in enumerate(crops)
            ]
        )
    )

    crop_result_card.set_visibility(True)


# =========================================================
# WEATHER DEMO
# =========================================================

def check_weather():

    weather_temperature.text = "27°C"
    weather_humidity.text = "72%"
    weather_rain.text = farmer_data["rainfall"]
    weather_condition.text = "ढगाळ"

    weather_message.text = (
        f"📍 ठिकाण: {farmer_data['location']}\n\n"
        "🌦️ सध्याचे हवामान: ढगाळ\n"
        "🌡️ तापमान: 27°C\n"
        "💧 आर्द्रता: 72%\n\n"
        "टीप: हे सध्या Demo Weather आहे. "
        "नंतर आपण Live Weather API जोडू शकतो."
    )

    weather_card.set_visibility(True)


# =========================================================
# DISEASE DEMO
# =========================================================

def disease_check():

    disease_result.text = (
        "🦠 संभाव्य रोग:\n\n"
        "पानांवरील डाग रोग\n\n"
        "🔍 सामान्य लक्षणे:\n"
        "• पानांवर तपकिरी डाग\n"
        "• पाने पिवळी पडणे\n"
        "• पाने वाळणे\n\n"
        "💡 प्राथमिक काळजी:\n"
        "• बाधित पाने वेगळी करा\n"
        "• शेतात योग्य निचरा ठेवा\n"
        "• पिकाची नियमित पाहणी करा\n"
        "• योग्य औषधासाठी कृषी तज्ज्ञांचा सल्ला घ्या\n\n"
        "⚠️ हे Demo Result आहे. "
        "नंतर आपण खरे AI Image Disease Model जोडू शकतो."
    )

    disease_result_card.set_visibility(True)


# =========================================================
# CSS
# =========================================================

ui.add_head_html("""
<style>

body {
    margin: 0;
    background: #f1f8f3;
    font-family: Arial, sans-serif;
}


/* HEADER */

.header {
    background: linear-gradient(
        90deg,
        #005c35,
        #008f4c,
        #006b3c
    );

    color: white;
    padding: 20px 35px;
}

.title {
    font-size: 30px;
    font-weight: bold;
}

.subtitle {
    font-size: 15px;
}


/* HERO */

.hero {
    background: linear-gradient(
        90deg,
        #dff5e4,
        #bfe8c8,
        #eaf8ed
    );

    padding: 45px;
}

.hero-title {
    font-size: 36px;
    font-weight: bold;
    color: #075c36;
    white-space: pre-line;
}

.hero-text {
    font-size: 18px;
    color: #315f45;
    white-space: pre-line;
}


/* CARD */

.main-card {
    background: white;
    border-radius: 18px;
    padding: 25px;

    box-shadow:
        0 4px 16px rgba(0,0,0,0.10);
}


/* STEP */

.step-title {
    font-size: 24px;
    font-weight: bold;
    color: #08733b;
}


/* WEATHER */

.weather {
    background: #eef8ff;
    border-radius: 18px;
    padding: 22px;
}


/* CROP */

.crop {
    background: #effbef;
    border-radius: 18px;
    padding: 22px;
}


/* DISEASE */

.disease {
    background: #faf4ff;
    border-radius: 18px;
    padding: 22px;
}


/* FOOTER */

.footer {
    background: #005c38;
    color: white;
    padding: 25px;
    text-align: center;
}


/* BUTTON */

button {
    font-weight: bold;
}


/* =====================================================
   MOBILE DESIGN
   ===================================================== */

@media (max-width: 768px) {

    body {
        background: #f1f8f3;
    }

    .header {
        padding: 15px;
    }

    .title {
        font-size: 23px;
    }

    .subtitle {
        font-size: 13px;
    }

    .hero {
        padding: 25px 18px;
    }

    .hero-title {
        font-size: 27px;
    }

    .hero-text {
        font-size: 15px;
    }

    .main-card {
        padding: 18px;
        border-radius: 15px;
    }

    .step-title {
        font-size: 20px;
    }

    button {
        min-height: 48px;
        font-size: 16px;
    }

    input {
        font-size: 16px !important;
    }

    .footer {
        padding: 18px;
        font-size: 14px;
    }

}

</style>
""")


# =========================================================
# HEADER
# =========================================================

with ui.element("div").classes(
    "header w-full"
):

    ui.label(
        "🌿 स्मार्ट शेतकरी सहाय्यक"
    ).classes("title")

    ui.label(
        "AI आधारित शेतकऱ्यांसाठी स्मार्ट मार्गदर्शन"
    ).classes("subtitle")


# =========================================================
# HERO
# =========================================================

with ui.element("div").classes(
    "hero w-full"
):

    ui.label(
        "शेतीत तंत्रज्ञानाची जोड,\n"
        "समृद्धीची नवी वाट!"
    ).classes("hero-title")

    ui.label(
        "हवामान • पिकांची शिफारस • रोग निदान\n"
        "शेतकऱ्यांसाठी सोपे आणि मराठी मार्गदर्शन"
    ).classes("hero-text")


# =========================================================
# MAIN
# =========================================================

with ui.column().classes(
    "w-full p-4 md:p-6"
):


    # =====================================================
    # FARMER FORM
    # =====================================================

    with ui.card().classes(
        "main-card w-full max-w-3xl mx-auto"
    ):

        ui.label(
            "👨‍🌾 शेतकऱ्याची माहिती"
        ).classes(
            "text-2xl font-bold text-green-700"
        )


        # -------------------------------------------------
        # STEP 1
        # -------------------------------------------------

        step1 = ui.column().classes("w-full")

        with step1:

            ui.label(
                "① तुमचे नाव"
            ).classes("step-title")

            name = ui.input(
                label="शेतकऱ्याचे नाव",
                placeholder="उदा. बाबासाहेब कुंभार"
            ).classes("w-full")

            ui.button(
                "पुढे ➜",
                on_click=next_name
            ).classes(
                "w-full bg-green-700 text-white"
            )


        # -------------------------------------------------
        # STEP 2
        # -------------------------------------------------

        step2 = ui.column().classes("w-full")

        step2.set_visibility(False)

        with step2:

            ui.label(
                "② मोबाईल नंबर"
            ).classes("step-title")

            mobile = ui.input(
                label="मोबाईल नंबर",
                placeholder="उदा. 9876543210"
            ).classes("w-full")

            with ui.row().classes("w-full"):

                ui.button(
                    "← मागे",
                    on_click=lambda: show_step(1)
                ).classes("flex-1")

                ui.button(
                    "पुढे ➜",
                    on_click=next_mobile
                ).classes(
                    "flex-1 bg-green-700 text-white"
                )


        # -------------------------------------------------
        # STEP 3
        # -------------------------------------------------

        step3 = ui.column().classes("w-full")

        step3.set_visibility(False)

        with step3:

            ui.label(
                "③ गाव / ठिकाण"
            ).classes("step-title")

            location = ui.input(
                label="गाव / ठिकाण",
                placeholder="उदा. राळेगण मसोबा"
            ).classes("w-full")

            with ui.row().classes("w-full"):

                ui.button(
                    "← मागे",
                    on_click=lambda: show_step(2)
                ).classes("flex-1")

                ui.button(
                    "पुढे ➜",
                    on_click=next_location
                ).classes(
                    "flex-1 bg-green-700 text-white"
                )


        # -------------------------------------------------
        # STEP 4
        # -------------------------------------------------

        step4 = ui.column().classes("w-full")

        step4.set_visibility(False)

        with step4:

            ui.label(
                "④ हंगाम"
            ).classes("step-title")

            season = ui.select(
                [
                    "पावसाळा",
                    "उन्हाळा",
                    "हिवाळा"
                ],
                value="पावसाळा",
                label="☀️ हंगाम निवडा"
            ).classes("w-full")

            with ui.row().classes("w-full"):

                ui.button(
                    "← मागे",
                    on_click=lambda: show_step(3)
                ).classes("flex-1")

                ui.button(
                    "पुढे ➜",
                    on_click=next_season
                ).classes(
                    "flex-1 bg-green-700 text-white"
                )


        # -------------------------------------------------
        # STEP 5
        # -------------------------------------------------

        step5 = ui.column().classes("w-full")

        step5.set_visibility(False)

        with step5:

            ui.label(
                "⑤ पावसाचे प्रमाण"
            ).classes("step-title")

            rainfall = ui.select(
                [
                    "जास्त",
                    "मध्यम",
                    "कमी"
                ],
                value="मध्यम",
                label="🌧️ पाऊस"
            ).classes("w-full")

            with ui.row().classes("w-full"):

                ui.button(
                    "← मागे",
                    on_click=lambda: show_step(4)
                ).classes("flex-1")

                ui.button(
                    "पुढे ➜",
                    on_click=next_rain
                ).classes(
                    "flex-1 bg-green-700 text-white"
                )


        # -------------------------------------------------
        # STEP 6
        # -------------------------------------------------

        step6 = ui.column().classes("w-full")

        step6.set_visibility(False)

        with step6:

            ui.label(
                "⑥ जमिनीचा प्रकार"
            ).classes("step-title")

            soil = ui.select(
                [
                    "कोरडवाहू",
                    "काळी माती",
                    "मध्यम",
                    "हलकी"
                ],
                value="मध्यम",
                label="🪨 जमीन"
            ).classes("w-full")

            with ui.row().classes("w-full"):

                ui.button(
                    "← मागे",
                    on_click=lambda: show_step(5)
                ).classes("flex-1")

                ui.button(
                    "पुढे ➜",
                    on_click=next_soil
                ).classes(
                    "flex-1 bg-green-700 text-white"
                )


        # -------------------------------------------------
        # STEP 7
        # -------------------------------------------------

        step7 = ui.column().classes("w-full")

        step7.set_visibility(False)

        with step7:

            ui.label(
                "⑦ पाण्याची उपलब्धता"
            ).classes("step-title")

            water = ui.select(
                [
                    "जास्त",
                    "मध्यम",
                    "कमी"
                ],
                value="मध्यम",
                label="💧 पाणी"
            ).classes("w-full")

            ui.button(
                "✅ माहिती पूर्ण करा",
                on_click=finish_farmer
            ).classes(
                "w-full bg-green-700 text-white"
            )


    # =====================================================
    # INFORMATION RESULT
    # =====================================================

    information_card = ui.card().classes(
        "main-card w-full max-w-3xl mx-auto mt-5"
    )

    information_card.set_visibility(False)

    with information_card:

        ui.label(
            "📋 तुमची माहिती"
        ).classes(
            "text-2xl font-bold text-green-700"
        )

        farmer_information = ui.label(
            ""
        ).classes(
            "whitespace-pre-line text-lg"
        )

        crop_button = ui.button(
            "🌱 पिकांची शिफारस करा",
            on_click=recommend_crops
        ).classes(
            "bg-green-700 text-white"
        )

        crop_button.set_visibility(False)


    # =====================================================
    # CROP RESULT
    # =====================================================

    crop_result_card = ui.card().classes(
        "crop w-full max-w-3xl mx-auto mt-5"
    )

    crop_result_card.set_visibility(False)

    with crop_result_card:

        ui.label(
            "🌱 पिकांची शिफारस"
        ).classes(
            "text-2xl font-bold text-green-800"
        )

        crop_result = ui.label(
            ""
        ).classes(
            "whitespace-pre-line text-lg"
        )


    # =====================================================
    # WEATHER
    # =====================================================

    weather_card = ui.card().classes(
        "weather w-full max-w-3xl mx-auto mt-5"
    )

    weather_card.set_visibility(False)

    with weather_card:

        ui.label(
            "🌦️ हवामानाची माहिती"
        ).classes(
            "text-2xl font-bold text-blue-800"
        )

        ui.button(
            "🌦️ हवामान तपासा",
            on_click=check_weather
        ).classes(
            "bg-blue-700 text-white"
        )

        with ui.row().classes(
            "w-full gap-3"
        ):

            with ui.card().classes("flex-1"):

                ui.label("🌡️ तापमान")

                weather_temperature = ui.label(
                    "--"
                ).classes(
                    "text-2xl font-bold text-blue-700"
                )


            with ui.card().classes("flex-1"):

                ui.label("💧 आर्द्रता")

                weather_humidity = ui.label(
                    "--"
                ).classes(
                    "text-2xl font-bold text-blue-700"
                )


            with ui.card().classes("flex-1"):

                ui.label("🌧️ पाऊस")

                weather_rain = ui.label(
                    "--"
                ).classes(
                    "text-2xl font-bold text-blue-700"
                )


            with ui.card().classes("flex-1"):

                ui.label("☁️ हवामान")

                weather_condition = ui.label(
                    "--"
                ).classes(
                    "text-2xl font-bold text-blue-700"
                )


        weather_message = ui.label(
            ""
        ).classes(
            "whitespace-pre-line text-blue-800"
        )


    # =====================================================
    # DISEASE DETECTION
    # =====================================================

    with ui.card().classes(
        "disease w-full max-w-3xl mx-auto mt-5"
    ):

        ui.label(
            "🦠 पिकाचा रोग निदान"
        ).classes(
            "text-2xl font-bold text-purple-700"
        )

        ui.label(
            "पिकाच्या पानाचा फोटो निवडा."
        )

        ui.upload(
            label="📷 पिकाचा फोटो निवडा",
            auto_upload=True
        ).classes("w-full")


        ui.button(
            "🔍 रोग तपासा",
            on_click=disease_check
        ).classes(
            "bg-purple-700 text-white"
        )


        disease_result_card = ui.card().classes(
            "w-full bg-purple-50"
        )

        disease_result_card.set_visibility(False)

        with disease_result_card:

            disease_result = ui.label(
                ""
            ).classes(
                "whitespace-pre-line"
            )


# =========================================================
# FOOTER
# =========================================================

with ui.element("div").classes(
    "footer w-full mt-8"
):

    ui.label(
        "🌿 शेतकऱ्यांच्या प्रगतीसाठी... नेहमी तुमच्या सेवेत!"
    ).classes("text-lg")

    ui.label(
        "Smart Farmer AI"
    )


# =========================================================
# STEPS
# =========================================================

steps = [
    step1,
    step2,
    step3,
    step4,
    step5,
    step6,
    step7
]


# =========================================================
# RUN
# =========================================================

ui.run(
    title="स्मार्ट शेतकरी सहाय्यक",
    host="0.0.0.0",
    port=8080,
    reload=False
)