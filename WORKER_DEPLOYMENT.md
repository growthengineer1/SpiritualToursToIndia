# Cloudflare Worker Deployment Instructions

## Your Worker is Ready! 🎉

The contact form email integration using Cloudflare Worker + SendGrid is complete.

## Files Created

- **`worker.js`** - The Cloudflare Worker code with SendGrid REST API integration

## What's Already Done ✅

1. ✅ Worker code created with SendGrid integration
2. ✅ Contact form updated to use Worker endpoint
3. ✅ JavaScript enhanced to handle JSON responses
4. ✅ CORS headers configured
5. ✅ Professional HTML email template
6. ✅ Error handling implemented

## How to Deploy the Worker

### Option 1: Cloudflare Dashboard (Easiest)

1. Go to [Cloudflare Workers Dashboard](https://dash.cloudflare.com/workers)
2. Click on your Worker: **spiritualtourstoindiaemail**
3. Click **"Quick Edit"** or **"Edit Code"**
4. Copy the entire contents of `worker.js` from this project
5. Paste into the Cloudflare code editor
6. Click **"Save and Deploy"**
7. Done! ✨

### Option 2: Wrangler CLI (Advanced)

```bash
# Install Wrangler (if not already installed)
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy the Worker
wrangler deploy worker.js --name spiritualtourstoindiaemail
```

## Environment Variables

**Already configured in Cloudflare:**
- ✅ `SENDGRID_API_KEY` - Your SendGrid API key (encrypted)

The Worker automatically accesses this via `env.SENDGRID_API_KEY`.

## Testing Your Worker

### 1. Test the Worker Directly

```bash
curl -X POST https://spiritualtourstoindiaemail.sabin.workers.dev \
  -d "name=Test User" \
  -d "email=test@example.com" \
  -d "message=This is a test message"
```

Expected response:
```json
{"success": true, "message": "Email sent successfully"}
```

### 2. Test from Your Website

1. Visit your website contact form
2. Fill in all required fields (name, email, message)
3. Click "Send Message"
4. You should see the success message
5. Check `hello@spiritualtourstoindia.com` for the email

## Email Details

- **From:** namaste@smukti.com
- **To:** hello@spiritualtourstoindia.com
- **Reply-To:** User's email address (automatically set)
- **Format:** Professional HTML with branded styling

## Troubleshooting

### Email not received?

1. **Check SendGrid Dashboard:**
   - Go to https://app.sendgrid.com/email_activity
   - Look for recent email activity
   - Check for bounce/block reasons

2. **Check Cloudflare Logs:**
   - Go to your Worker in Cloudflare Dashboard
   - Click "Logs" tab
   - Look for errors during form submission

3. **Verify SendGrid API Key:**
   - Ensure it's not expired
   - Check it has "Mail Send" permissions
   - Verify "from" address (namaste@smukti.com) is verified in SendGrid

### Common Issues

**Issue:** CORS error in browser console
- **Solution:** Worker includes CORS headers, but verify browser isn't blocking

**Issue:** 401 Unauthorized from SendGrid
- **Solution:** SendGrid API key invalid/expired - regenerate in SendGrid settings

**Issue:** 400 Bad Request
- **Solution:** Check form field names match Worker expectations (name, email, message)

## Next Steps

1. **Deploy the Worker** using Option 1 or 2 above
2. **Test the form** on your live website
3. **Monitor initial submissions** to ensure everything works
4. **Consider adding**:
   - Rate limiting (prevent spam)
   - HTML escaping for message content (security)
   - Custom email templates for different form types

## Support

If you encounter issues:
- Check Cloudflare Worker logs
- Check SendGrid email activity logs
- Verify environment variables are set correctly

---

**Your contact form is now powered by your own Worker!** No third-party dependencies, full control, professional emails. 🚀
