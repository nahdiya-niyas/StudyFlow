/* =========================================================
   STUDYFLOW — INTERACTIONS
   ========================================================= */


/* =========================================================
   PROFESSIONAL CONFIRMATION
   ========================================================= */

function showConfirm(title, message) {

    return new Promise(resolve => {

        const overlay = document.createElement("div");

        overlay.className = "confirm-overlay";

        overlay.innerHTML = `
            <div class="confirm-box">

                <div class="confirm-icon">
                    ⚠️
                </div>

                <h2>${title}</h2>

                <p>${message}</p>

                <div class="confirm-actions">

                    <button type="button" class="confirm-cancel">
                        Cancel
                    </button>

                    <button type="button" class="confirm-danger">
                        Delete
                    </button>

                </div>

            </div>
        `;

        document.body.appendChild(overlay);

        const cancelButton =
            overlay.querySelector(".confirm-cancel");

        const deleteButton =
            overlay.querySelector(".confirm-danger");


        cancelButton.addEventListener("click", function () {

            overlay.remove();

            document.body.style.overflow = "";

            resolve(false);

        });


        deleteButton.addEventListener("click", function () {

            overlay.remove();

            document.body.style.overflow = "";

            resolve(true);

        });


        overlay.addEventListener("click", function (event) {

            if (event.target === overlay) {

                overlay.remove();

                document.body.style.overflow = "";

                resolve(false);

            }

        });

    });

}


/* =========================================================
   MESSAGE BOX
   ========================================================= */

function showMessage(message, title = "StudyFlow") {

    const overlay = document.createElement("div");

    overlay.className = "message-overlay";

    overlay.innerHTML = `
        <div class="message-box">

            <div class="message-icon">
                ℹ️
            </div>

            <h2>${title}</h2>

            <p>${message}</p>

            <button
                type="button"
                class="primary-btn message-ok"
            >
                OK
            </button>

        </div>
    `;

    document.body.appendChild(overlay);

    const button =
        overlay.querySelector(".message-ok");

    button.addEventListener("click", function () {

        overlay.remove();

    });

}


/* =========================================================
   DELETE NOTE
   ========================================================= */

async function deleteNote(noteId) {

    if (!noteId) {
        console.error("Missing note ID.");
        return;
    }


    const confirmed = await showConfirm(
        "Delete Note?",
        "Are you sure you want to permanently delete this note?"
    );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            "/delete-note",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    noteId: noteId
                })
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to delete note."
            );

        }


        const noteCard =
            document.getElementById(
                "note-" + noteId
            );


        if (noteCard) {

            noteCard.style.transition =
                "opacity 0.25s ease, transform 0.25s ease";

            noteCard.style.opacity = "0";

            noteCard.style.transform =
                "translateY(10px)";


            setTimeout(function () {

                noteCard.remove();

                updateNoteCount();

            }, 250);

        } else {

            window.location.reload();

        }


    } catch (error) {

        console.error(
            "Delete note error:",
            error
        );

        showMessage(
            error.message ||
            "Something went wrong while deleting the note."
        );

    }

}


/* =========================================================
   UPDATE NOTE COUNT
   ========================================================= */

function updateNoteCount() {

    const notes =
        document.querySelectorAll(".note-card");

    const count =
        document.getElementById("notes-count");


    if (count) {

        const total = notes.length;

        count.textContent =
            total +
            (total === 1 ? " note" : " notes");

    }


    if (notes.length === 0) {

        const notesList =
            document.getElementById("notes-list");


        if (notesList) {

            notesList.innerHTML = `

                <div class="empty-state">

                    <div>
                        📝
                    </div>

                    <h3>
                        No notes yet
                    </h3>

                    <p>
                        Create your first note.
                    </p>

                </div>

            `;

        }

    }

}


/* =========================================================
   PIN NOTE
   ========================================================= */

async function togglePin(noteId) {

    if (!noteId) {
        return;
    }


    try {

        const response = await fetch(
            "/toggle-pin/" + noteId,
            {
                method: "POST"
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to pin note."
            );

        }


        window.location.reload();


    } catch (error) {

        console.error(
            "Pin error:",
            error
        );

        showMessage(
            error.message ||
            "Something went wrong."
        );

    }

}


/* =========================================================
   FAVORITE NOTE
   ========================================================= */

async function toggleFavorite(noteId) {

    if (!noteId) {
        return;
    }


    try {

        const response = await fetch(
            "/toggle-favorite/" + noteId,
            {
                method: "POST"
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to favorite note."
            );

        }


        window.location.reload();


    } catch (error) {

        console.error(
            "Favorite error:",
            error
        );

        showMessage(
            error.message ||
            "Something went wrong."
        );

    }

}


/* =========================================================
   TASK — COMPLETE
   ========================================================= */

async function completeTask(taskId) {

    if (!taskId) {
        return;
    }


    try {

        const response = await fetch(
            `/tasks/complete/${taskId}`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                }
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Could not update task."
            );

        }


        window.location.reload();


    } catch (error) {

        console.error(
            "Complete task error:",
            error
        );

        showMessage(
            error.message ||
            "Something went wrong."
        );

    }

}


/* =========================================================
   TASK — DELETE
   ========================================================= */

async function deleteTask(taskId) {

    if (!taskId) {
        return;
    }


    const confirmed = await showConfirm(
        "Delete Task?",
        "Are you sure you want to permanently delete this task?"
    );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `/tasks/delete/${taskId}`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                }
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Could not delete task."
            );

        }


        window.location.reload();


    } catch (error) {

        console.error(
            "Delete task error:",
            error
        );

        showMessage(
            error.message ||
            "Could not delete the task."
        );

    }

}


/* =========================================================
   PLANNER — START SESSION
   ========================================================= */

async function startSession(sessionId, button) {

    if (!sessionId || !button) {
        return;
    }


    button.disabled = true;

    const originalText =
        button.innerHTML;

    button.innerHTML =
        "Starting...";


    try {

        const response = await fetch(
            `/planner/start/${sessionId}`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                }
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Could not start session."
            );

        }


        window.location.reload();


    } catch (error) {

        console.error(
            "Start session error:",
            error
        );

        showMessage(
            error.message ||
            "Something went wrong."
        );

        button.disabled = false;

        button.innerHTML =
            originalText;

    }

}


/* =========================================================
   PLANNER — DELETE SESSION
   ========================================================= */

async function deleteSession(sessionId) {

    if (!sessionId) {
        return;
    }


    const confirmed = await showConfirm(
        "Delete Study Session?",
        "Are you sure you want to permanently delete this study session?"
    );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `/planner/delete/${sessionId}`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                }
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Could not delete session."
            );

        }


        window.location.reload();


    } catch (error) {

        console.error(
            "Delete session error:",
            error
        );

        showMessage(
            error.message ||
            "Could not delete the session."
        );

    }

}


/* =========================================================
   MAKE FUNCTIONS AVAILABLE TO HTML
   ========================================================= */

window.showConfirm = showConfirm;
window.showMessage = showMessage;

window.deleteNote = deleteNote;
window.updateNoteCount = updateNoteCount;

window.togglePin = togglePin;
window.toggleFavorite = toggleFavorite;

window.completeTask = completeTask;
window.deleteTask = deleteTask;

window.startSession = startSession;
window.deleteSession = deleteSession;