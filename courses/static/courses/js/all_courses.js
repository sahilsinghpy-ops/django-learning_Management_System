window.onload = async function () {
    await loadAllCourses();
}

async function logout() {
    await fetch('/users/logout/', {
        method: 'POST',
        credentials: 'include'
    });
    window.location.href = '/users/login-page/';
}

async function loadAllCourses() {
    try {
        const res = await fetch('/courses/', {
            credentials: 'include'
        });

        if (res.status === 401 || res.status === 403) {
            window.location.href = '/users/login-page/';
            return;
        }

        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            document.getElementById('allCoursesGrid').innerHTML = '<p style="color:red">Session expired. <a href="/users/login-page/">Login again</a></p>';
            return;
        }

        const data = await res.json();
        const grid = document.getElementById('allCoursesGrid');
        grid.innerHTML = '';

        if (data.length === 0) {
            grid.innerHTML = '<p style="color:#999">No courses available yet.</p>';
            return;
        }

        data.forEach(course => {
    grid.innerHTML += `
        <div class="course-card">
            <span class="badge">${course.category_name || 'No Category'}</span>
            <h3>${course.Title}</h3>
            <p>${course.Description}</p>
            <p style="font-size:13px; color:#999">
                👨‍🏫 ${course.teacher_name} &nbsp;|&nbsp;
                📚 ${course.lessons.length} lessons &nbsp;|&nbsp;
                ⭐ ${course.average_rating}
            </p>
            <div class="actions" style="margin-top:10px">
                <button class="btn btn-primary" onclick="window.location.href='/courses/detail/${course.id}/'">View Course</button>
                <button class="btn btn-success" onclick="enroll(${course.id}, this)">Enroll</button>
            </div>
        </div>
    `;
});

    } catch (err) {
        console.error('Error:', err);
        document.getElementById('allCoursesGrid').innerHTML = '<p style="color:red">Something went wrong. <a href="/users/login-page/">Login again</a></p>';
    }
}

async function enroll(courseId, btn) {
    btn.disabled = true;
    btn.textContent = 'Enrolling...';

    try {
        const res = await fetch(`/courses/${courseId}/enroll/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });

        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            btn.disabled = false;
            btn.textContent = 'Enroll';
            alert('Session expired. Please login again.');
            return;
        }

        const result = await res.json();

        if (res.ok) {
            btn.textContent = 'Enrolled ✓';
            btn.style.background = '#95a5a6';
        } else {
            btn.disabled = false;
            btn.textContent = 'Enroll';
            alert(result.error || 'Something went wrong');
        }

    } catch (err) {
        btn.disabled = false;
        btn.textContent = 'Enroll';
        alert('Something went wrong. Please try again.');
    }
}