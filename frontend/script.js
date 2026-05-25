const API_URL = "http://127.0.0.1:8000";

let calendar;

document.addEventListener("DOMContentLoaded", async () => {

    const modal =
        document.getElementById("eventModal");

    const addBtn =
        document.getElementById("addEventBtn");

    const closeBtn =
        document.getElementById("closeModal");

    const saveBtn =
        document.getElementById("saveBtn");

    addBtn.addEventListener("click", () => {

        clearForm();

        modal.style.display = "flex";
    });

    closeBtn.addEventListener("click", () => {

        modal.style.display = "none";
    });

    window.addEventListener("click", (e) => {

        if (e.target === modal) {

            modal.style.display = "none";
        }
    });

    saveBtn.addEventListener(
        "click",
        saveEvent
    );

    await initializeCalendar();
});

async function initializeCalendar() {

    const calendarEl =
        document.getElementById("calendar");

    const events =
        await fetchEvents();

    calendar =
        new FullCalendar.Calendar(
            calendarEl,
            {
                initialView: "dayGridMonth",

                height: "auto",

                editable: false,

                selectable: true,

                displayEventTime: false,

                headerToolbar: {
                    left: "prev,next today",
                    center: "title",
                    right: "dayGridMonth,timeGridWeek,timeGridDay"
                },

                events: events,

                dateClick(info) {

                    clearForm();

                    document
                        .getElementById(
                            "start_time"
                        ).value =
                        info.dateStr +
                        "T09:00";

                    document
                        .getElementById(
                            "end_time"
                        ).value =
                        info.dateStr +
                        "T10:00";

                    document
                        .getElementById(
                            "eventModal"
                        ).style.display =
                        "flex";
                },

                eventClick(info) {

                    alert(
                        "Event: " +
                        info.event.title
                    );
                }
            }
        );

    calendar.render();
}

async function fetchEvents() {

    try {

        const response =
            await fetch(
                `${API_URL}/events`
            );

        const data =
            await response.json();

        return data.map(event => ({

            id: event.id,

            title: event.title,

            start: event.start_time,

            end: event.end_time
        }));

    } catch (error) {

        console.error(error);

        return [];
    }
}

async function saveEvent() {

    const title =
        document
        .getElementById("title")
        .value
        .trim();

    const description =
        document
        .getElementById("description")
        .value
        .trim();

    const start_time =
        document
        .getElementById("start_time")
        .value;

    const end_time =
        document
        .getElementById("end_time")
        .value;

    if (!title) {

        alert(
            "Please enter event title"
        );

        return;
    }

    if (!start_time || !end_time) {

        alert(
            "Select start and end time"
        );

        return;
    }

    const payload = {

        title,

        description,

        start_time,

        end_time
    };

    try {

        const response =
            await fetch(
                `${API_URL}/events`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );

        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }

        alert(
            "Event Added Successfully"
        );

        document
            .getElementById(
                "eventModal"
            ).style.display =
            "none";

        clearForm();

        calendar.destroy();

        await initializeCalendar();

    } catch (err) {

        console.error(err);

        alert(
            "Failed to save event"
        );
    }
}

function clearForm() {

    document
        .getElementById("title")
        .value = "";

    document
        .getElementById("description")
        .value = "";

    document
        .getElementById("start_time")
        .value = "";

    document
        .getElementById("end_time")
        .value = "";
}