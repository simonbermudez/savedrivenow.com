# Cloudflare Turnstile CAPTCHA Setup

This project uses Cloudflare Turnstile CAPTCHA to protect the lead generation form from bot submissions.

## Getting Started

### 1. Get Cloudflare Turnstile Keys

1. Go to the [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Select "Turnstile" from the sidebar
3. Click "Add a site"
4. Enter your domain (e.g., `savedrivenow.siber.live`)
5. For development, you can use `localhost` or `127.0.0.1`
6. Copy the **Site Key** and **Secret Key**

### 2. Update Environment Variables

Update your `.env` file with the actual keys:

```env
TURNSTILE_SITE_KEY=your_actual_site_key_here
TURNSTILE_SECRET_KEY=your_actual_secret_key_here
```

### 3. Test Keys (Development Only)

For testing purposes, Cloudflare provides test keys that always pass:
- Site Key: `1x00000000000000000000AA` (always passes)
- Secret Key: `1x0000000000000000000000000000000AA` (always passes)

For testing failures:
- Site Key: `2x00000000000000000000AB` (always fails)
- Secret Key: `2x0000000000000000000000000000000AB` (always fails)

### 4. Production Configuration

For production deployment:
1. Use your actual domain when creating the Turnstile site
2. Replace the test keys with your actual keys
3. Make sure the domain matches exactly (including www if applicable)

## How It Works

1. The CAPTCHA widget is displayed on the landing form
2. Users must complete the CAPTCHA before submitting
3. The form submission includes the CAPTCHA response token
4. Django validates the token with Cloudflare's API
5. Only valid submissions are processed

## Customization

The CAPTCHA appearance can be customized by modifying the widget attributes in `leads/turnstile.py`:

- `data-theme`: "light", "dark", or "auto"
- `data-size`: "normal", "compact", or "flexible"
- `data-appearance`: "always", "execute", or "interaction-only"

## Troubleshooting

### Common Issues

1. **CAPTCHA not loading**: Check that the site key is correct and the domain is authorized
2. **Validation failing**: Verify the secret key and ensure the token is being passed correctly
3. **Development issues**: Use the test keys provided above for local testing

### Error Messages

- `CAPTCHA verification is required.`: User didn't complete the CAPTCHA
- `CAPTCHA has expired. Please try again.`: Token expired (default: 5 minutes)
- `Invalid CAPTCHA response. Please try again.`: Malformed or invalid token
- `CAPTCHA verification failed. Please try again.`: Network error or server issue

## Security Notes

- Never expose your secret key in client-side code
- The secret key should only be used on your server
- Regularly rotate your keys if needed
- Monitor your Turnstile dashboard for usage statistics and potential abuse
