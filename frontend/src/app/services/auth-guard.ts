import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

// Helper function to check if the JWT has expired
function isTokenExpired(token: string): boolean {
  try {
    // 1. Grab the middle part (the payload)
    const payloadBase64 = token.split('.')[1];
    // 2. Decode the Base64 string into plain text
    const decodedJson = atob(payloadBase64);
    // 3. Parse into a JavaScript object
    const payload = JSON.parse(decodedJson);
    
    // 'exp' is stored in seconds, but JavaScript uses milliseconds (multiply by 1000)
    return payload.exp * 1000 < Date.now();
  } catch (err) {
    // If the token is corrupted or invalid, treat it as expired
    return true;
  }
}

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');

  // Check BOTH: does it exist AND is it still valid?
  if (token && !isTokenExpired(token)) {
    return true; // Valid token, welcome!
  } else {
    // Automatically wipe the stale/expired token so it doesn't linger!
    localStorage.removeItem('token');
    router.navigate(['/login']);
    return false; // Block access!
  }
};