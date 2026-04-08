let allCourses = [];
let categories = [];
let selectedCourseId = null;

window.onload = async function () {
    const role = localStorage.getItem('role');
    const username = localStorage.getItem('username');
    
    console.log('Role:', role);
    console.log('Username:', username);
    if (!role || role !== 'teacher') {
        window.location.href = '/users/login-page/';
        return;
    }

    // Show username and first letter icon
    document.getElementById('navUsername').textContent = username;
    document.getElementById('navIcon').textContent = username.charAt(0).toUpperCase();

    await loadCategories();
    await loadMyCourses();
}

async function logout() {
    await fetch('/users/logout/', {
        method: 'POST',
        credentials: 'include'
    });
    window.location.href = '/users/login-page/';
}

async function loadCategories() {
    try {
        const res = await fetch('/courses/categories/', {
            credentials: 'include'
        });
        categories = await res.json();
        const select = document.getElementById('courseCategory');
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.name;
            select.appendChild(option);
        });
    } catch (err) {
        console.error('Error loading categories:', err);
    }
}

async function loadMyCourses() {
    try {
        const res = await fetch('/courses/my-courses/', {
            credentials: 'include'
        });

        if (res.status === 401) {
            window.location.href = '/users/login-page/';
            return;
        }

        const data = await res.json();
        allCourses = data;
        renderCourses(data);
    } catch (err) {
        console.error('Error loading courses:', err);
    }
}

function renderCourses(courses) {
    const grid = document.getElementById('coursesGrid');
    grid.innerHTML = '';

    if (courses.length === 0) {
        grid.innerHTML = '<p style="color:#999">No courses yet. Create your first course!</p>';
        return;
    }

    courses.forEach(course => {
    grid.innerHTML += `
        <div class="course-card">
            <span class="badge">${course.category_name || 'No Category'}</span>
            <h3>${course.Title}</h3>
            <p>${course.Description}</p>
            <p style="font-size:13px; color:#999">${course.lessons.length} lessons</p>
            <div class="actions" style="margin-top:10px">
                <button class="btn btn-primary" onclick="window.location.href='/courses/detail/${course.id}/'">View Course</button>
                <button class="btn btn-success" onclick="openLessonModal(${course.id})">Add Lesson</button>
            </div>
        </div>
    `;
});
}

function openCourseModal() {
    document.getElementById('courseModal').classList.add('active');
}

function closeCourseModal() {
    document.getElementById('courseModal').classList.remove('active');
    document.getElementById('courseError').style.display = 'none';
}

async function createCourse() {
    const errorMsg = document.getElementById('courseError');
    errorMsg.style.display = 'none';

    const data = {
        Title: document.getElementById('courseTitle').value,
        Description: document.getElementById('courseDesc').value,
        category: document.getElementById('courseCategory').value,
    };

    try {
        const res = await fetch('/courses/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok) {
            closeCourseModal();
            await loadMyCourses();
        } else {
            let errors = '';
            for (let key in result) errors += result[key] + ' ';
            errorMsg.textContent = errors;
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        errorMsg.textContent = 'Something went wrong. Please try again.';
        errorMsg.style.display = 'block';
    }
}

function openLessonModal(courseId) {
    selectedCourseId = courseId;
    document.getElementById('lessonModal').classList.add('active');
}

function closeLessonModal() {
    document.getElementById('lessonModal').classList.remove('active');
    document.getElementById('lessonError').style.display = 'none';
    selectedCourseId = null;
}

async function createLesson() {
    const errorMsg = document.getElementById('lessonError');
    errorMsg.style.display = 'none';

    const data = {
        title: document.getElementById('lessonTitle').value,
        content: document.getElementById('lessonContent').value,
        video_url: document.getElementById('lessonVideo').value,
        order: document.getElementById('lessonOrder').value,
    };

    try {
        const res = await fetch(`/courses/${selectedCourseId}/lessons/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok) {
            closeLessonModal();
            await loadMyCourses();
        } else {
            let errors = '';
            for (let key in result) errors += result[key] + ' ';
            errorMsg.textContent = errors;
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        errorMsg.textContent = 'Something went wrong. Please try again.';
        errorMsg.style.display = 'block';
    }
}