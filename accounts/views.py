from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.core.cache import cache
import time

def login_view(request):
    lockout_remaining = 0

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        lock_key = f"login_lockout_{username}"
        attempt_key = f"failed_login_attempts_{username}"

        if cache.get(lock_key):
            expiry_time = cache.get(f"{lock_key}_expiry", 0)
            time_left = int(expiry_time - time.time())
            
            if time_left > 0:
                messages.error(request, "ACCOUNT LOCKED OUT. Security throttling active.")
                return render(request, 'accounts/login.html', {'lockout_remaining': time_left})
            else:
                cache.delete(lock_key)
                cache.delete(f"{lock_key}_expiry")

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            cache.delete(attempt_key)
            cache.delete(lock_key)
            cache.delete(f"{lock_key}_expiry")
            auth.login(request, user)
            return redirect('/admin/') 
        else:
            failures = cache.get(attempt_key, 0) + 1
            cache.set(attempt_key, failures, timeout=300)

            if failures >= 5:
                cache.set(lock_key, True, timeout=30)
                cache.set(f"{lock_key}_expiry", time.time() + 30, timeout=30)
                messages.error(request, "Too many bad login attempts. PAX CONTROL has locked this account route.")
                lockout_remaining = 30
            else:
                remaining_attempts = 5 - failures
                messages.error(request, f"Invalid credentials. You have {remaining_attempts} attempts remaining.")

    return render(request, 'accounts/login.html', {'lockout_remaining': lockout_remaining})

def signup_view(request):
    if request.method == "POST":
        messages.success(request, "Identity provisioned successfully. Please authenticate.")
        return redirect('login')
    return render(request, 'accounts/signup.html')