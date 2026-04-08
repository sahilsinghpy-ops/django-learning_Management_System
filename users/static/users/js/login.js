async function login() {
    const errorMsg = document.getElementById('errorMsg');
    errorMsg.style.display = 'none';

    const data = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/users/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            // Save to localStorage
            localStorage.setItem('username', result.username);
            localStorage.setItem('role', result.role);

            if (result.role === 'teacher') {
                window.location.href = '/courses/teacher/dashboard/';
            } else {
                window.location.href = '/courses/student/dashboard/';
            }
        } else {
            errorMsg.textContent = result.error || 'Invalid credentials';
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        errorMsg.textContent = 'Something went wrong. Please try again.';
        errorMsg.style.display = 'block';
    }
}