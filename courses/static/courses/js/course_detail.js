const courseId = window.location.pathname.split('/').filter(Boolean).pop();

window.onload = async function () {
    const username = localStorage.getItem('username');
    const role = localStorage.getItem('role');

    if (!username) {
        window.location.href = '/users/login-page/';
        return;
    }

    document.getElementById('navUsername').textContent = username;
    document.getElementById('navIcon').textContent = username.charAt(0).toUpperCase();

    await loadCourseDetail();
}

function goBack() {
    const role = localStorage.getItem('role');
    if (role === 'teacher') {
        window.location.href = '/courses/teacher/dashboard/';
    } else {
        window.location.href = '/courses/all/';
    }
}

async function logout() {
    await fetch('/users/logout/', {
        method: 'POST',
        credentials: 'include'
    });
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    window.location.href = '/users/login-page/';
}

async function loadCourseDetail() {
    try {
        const res = await fetch(`/courses/${courseId}/`, {
            credentials: 'include'
        });

        if (!res.ok) {
            document.getElementById('courseHeader').innerHTML = '<p style="color:red">Failed to load course.</p>';
            return;
        }

        const course = await res.json();
        const role = localStorage.getItem('role');

        document.getElementById('courseTitle').textContent = course.Title;

        document.getElementById('courseHeader').innerHTML = `
            <h2>${course.Title}</h2>
            <p>${course.Description}</p>
            <p style="font-size:13px; margin-top:10px; color:#999">
                👨‍🏫 ${course.teacher_name} &nbsp;|&nbsp;
                📚 ${course.lessons.length} lessons &nbsp;|&nbsp;
                ⭐ ${course.average_rating}
            </p>
        `;

        const lessonList = document.getElementById('lessonList');
        lessonList.innerHTML = '';

        if (course.lessons.length === 0) {
            lessonList.innerHTML = '<p style="color:#999">No lessons yet.</p>';
            return;
        }

        course.lessons.forEach((lesson, index) => {
            lessonList.innerHTML += `
                <div class="lesson-item">
                    <div class="lesson-number">${index + 1}</div>
                    <div class="lesson-info">
                        <h4>${lesson.title}</h4>
                        <p>${lesson.content}</p>
                        ${lesson.video_url ? `<a href="${lesson.video_url}" target="_blank">▶ Watch Video</a>` : ''}
                    </div>
                    ${role === 'teacher' ? `
                    <div style="margin-left:auto">
                        <button class="btn btn-primary" onclick="openEditModal(${lesson.id}, '${lesson.title}', '${lesson.content}', '${lesson.video_url}', ${lesson.order})">Edit</button>
                        <button class="btn btn-danger" onclick="deleteLesson(${lesson.id})" style="margin-top:5px">Delete</button>
                    </div>` : ''}
                </div>
            `;
        });

    } catch (err) {
        console.error('Error:', err);
    }
}

// Edit Modal
function openEditModal(id, title, content, video_url, order) {
    document.getElementById('editLessonId').value = id;
    document.getElementById('editTitle').value = title;
    document.getElementById('editContent').value = content;
    document.getElementById('editVideoUrl').value = video_url;
    document.getElementById('editOrder').value = order;
    document.getElementById('editModal').classList.add('active');
}

function closeEditModal() {
    document.getElementById('editModal').classList.remove('active');
}

async function updateLesson() {
    const lessonId = document.getElementById('editLessonId').value;
    const errorMsg = document.getElementById('editError');
    errorMsg.style.display = 'none';

    const data = {
        title: document.getElementById('editTitle').value,
        content: document.getElementById('editContent').value,
        video_url: document.getElementById('editVideoUrl').value,
        order: document.getElementById('editOrder').value,
    };

    try {
        const res = await fetch(`/courses/${courseId}/lessons/${lessonId}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok) {
            closeEditModal();
            await loadCourseDetail();
        } else {
            let errors = '';
            for (let key in result) errors += result[key] + ' ';
            errorMsg.textContent = errors;
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        errorMsg.textContent = 'Something went wrong.';
        errorMsg.style.display = 'block';
    }
}

async function deleteLesson(lessonId) {
    if (!confirm('Are you sure you want to delete this lesson?')) return;

    try {
        const res = await fetch(`/courses/${courseId}/lessons/${lessonId}/`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (res.ok) {
            await loadCourseDetail();
        } else {
            alert('Failed to delete lesson.');
        }
    } catch (err) {
        alert('Something went wrong.');
    }
}