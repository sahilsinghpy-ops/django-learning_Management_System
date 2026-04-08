window.onload = async function () {
    const role = localStorage.getItem('role');
    const username = localStorage.getItem('username');

    if (!role || role !== 'student') {
        window.location.href = '/users/login-page/';
        return;
    }

    // Show username and first letter icon
    document.getElementById('navUsername').textContent = username;
    document.getElementById('navIcon').textContent = username.charAt(0).toUpperCase();

    await loadEnrolledCourses();
}

async function logout() {
    await fetch('/users/logout/', {
        method: 'POST',
        credentials: 'include'
    });
    window.location.href = '/users/login-page/';
}

async function loadEnrolledCourses() {
    try {
        const res = await fetch('/courses/enrollments/', {
            credentials: 'include'
        });

        if (res.status === 401 || res.status === 403) {
            window.location.href = '/users/login-page/';
            return;
        }

        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            document.getElementById('enrolledGrid').innerHTML = '<p style="color:red">Session expired. <a href="/users/login-page/">Login again</a></p>';
            return;
        }

        const data = await res.json();
        const grid = document.getElementById('enrolledGrid');
        grid.innerHTML = '';

        if (data.length === 0) {
            grid.innerHTML = `
                <p style="color:#999">
                    You are not enrolled in any courses yet. 
                    <a href="/courses/all/">Browse courses</a>
                </p>`;
            return;
        }

       data.forEach(enrollment => {
    grid.innerHTML += `
        <div class="course-card">
            <h3>${enrollment.course_title}</h3>
            <p>Enrolled on: ${new Date(enrollment.created_at).toLocaleDateString()}</p>
            <div class="actions" style="margin-top:10px">
                <button class="btn btn-primary" onclick="window.location.href='/courses/detail/${enrollment.course}/'">View Lessons</button>
                <button class="btn btn-success" onclick="openReviewModal(${enrollment.course})">Add Review</button>
            </div>
        </div>
    `;
});

    } catch (err) {
        console.error('Error:', err);
        document.getElementById('enrolledGrid').innerHTML = '<p style="color:red">Something went wrong. <a href="/users/login-page/">Login again</a></p>';
    }
}

function openReviewModal(courseId) {
    document.getElementById('selectedCourseId').value = courseId;
    document.getElementById('reviewModal').classList.add('active');
}

function closeReviewModal() {
    document.getElementById('reviewModal').classList.remove('active');
    document.getElementById('reviewError').style.display = 'none';
}

async function submitReview() {
    const courseId = document.getElementById('selectedCourseId').value;
    const errorMsg = document.getElementById('reviewError');
    errorMsg.style.display = 'none';

    const data = {
        rating: document.getElementById('rating').value,
        comment: document.getElementById('comment').value,
    };

    try {
        const res = await fetch(`/courses/${courseId}/reviews/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });

        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            errorMsg.textContent = 'Session expired. Please login again.';
            errorMsg.style.display = 'block';
            return;
        }

        const result = await res.json();

        if (res.ok) {
            closeReviewModal();
            alert('Review submitted successfully!');
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