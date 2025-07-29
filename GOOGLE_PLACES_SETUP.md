# Google Places API Setup

To enable address autocomplete and validation, you need to set up the Google Places API.

## Steps to Setup:

1. **Go to Google Cloud Console**: https://console.cloud.google.com/

2. **Create a new project** (or use existing one):
   - Click "Select a project" → "New Project"
   - Enter project name and click "Create"

3. **Enable the Places API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Places API"
   - Click on "Places API" and click "Enable"

4. **Create API Key**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the generated API key

5. **Restrict the API Key** (Recommended for security):
   - Click on the API key to edit it
   - Under "Application restrictions":
     - Select "HTTP referrers (web sites)"
     - Add your domain(s): `yourdomain.com/*`, `*.yourdomain.com/*`
   - Under "API restrictions":
     - Select "Restrict key"
     - Check "Places API"
   - Click "Save"

6. **Set the Environment Variable**:
   ```bash
   export GOOGLE_PLACES_API_KEY="your_actual_api_key_here"
   ```

   Or add it to your `.env` file:
   ```
   GOOGLE_PLACES_API_KEY=your_actual_api_key_here
   ```

## Features Enabled:

- ✅ **Address Autocomplete**: Users can start typing an address and get suggestions
- ✅ **Auto-fill Fields**: When an address is selected, city, state, and ZIP are automatically filled
- ✅ **Address Validation**: Real-time validation of address components
- ✅ **ZIP Code Validation**: Validates ZIP code format (12345 or 12345-6789)
- ✅ **US Address Only**: Restricted to US addresses for insurance purposes
- ✅ **Visual Feedback**: Green/red borders indicate valid/invalid fields

## Testing:

1. Start the development server: `python manage.py runserver`
2. Go to the landing page
3. Start typing an address in the "Street Address" field
4. Select an address from the dropdown
5. Verify that city, state, and ZIP code are automatically filled

## Troubleshooting:

- **No autocomplete suggestions**: Check if the API key is valid and Places API is enabled
- **Console errors**: Check browser developer tools for any JavaScript errors
- **Address not found**: Make sure you're entering a valid US address

## Cost Considerations:

- Google Places API has usage-based pricing
- Consider setting up billing alerts and quotas
- The first $200 per month is free for most users
- Each autocomplete session costs approximately $0.017

## Security Notes:

- Never commit your API key to version control
- Use environment variables or secure secret management
- Restrict the API key to specific domains and APIs
- Monitor usage in Google Cloud Console
