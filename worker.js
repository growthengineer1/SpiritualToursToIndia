// Cloudflare Worker for Contact Form Email via SendGrid
// Deploy this to: spiritualtourstoindiaemail.sabin@nguserv.workers.dev

export default {
  async fetch(request, env) {
    // Handle CORS preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    // Only allow POST requests
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ success: false, error: 'Method not allowed' }), {
        status: 405,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }

    try {
      // Parse form data
      const formData = await request.formData();
      const name = formData.get('name')?.trim();
      const email = formData.get('email')?.trim();
      const message = formData.get('message')?.trim();

      // Validate required fields
      if (!name || !email || !message) {
        return new Response(JSON.stringify({ 
          success: false, 
          error: 'All fields are required' 
        }), {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        return new Response(JSON.stringify({ 
          success: false, 
          error: 'Invalid email address' 
        }), {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      // Send email via SendGrid REST API
      const sendGridResponse = await fetch('https://api.sendgrid.com/v3/mail/send', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.SENDGRID_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          personalizations: [{
            to: [{ email: 'hello@spiritualtourstoindia.com' }],
            subject: `New Contact Form Submission from ${name}`,
          }],
          from: {
            email: 'namaste@smukti.com',
            name: 'Spiritual Tours to India'
          },
          reply_to: {
            email: email,
            name: name
          },
          content: [{
            type: 'text/html',
            value: `
              <!DOCTYPE html>
              <html>
              <head>
                <style>
                  body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                  .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                  .header { background-color: #ea580c; color: white; padding: 20px; border-radius: 5px 5px 0 0; }
                  .content { background-color: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }
                  .field { margin-bottom: 20px; }
                  .label { font-weight: bold; color: #6b7280; text-transform: uppercase; font-size: 12px; margin-bottom: 5px; }
                  .value { font-size: 16px; color: #111827; }
                  .message-box { background-color: white; padding: 15px; border-left: 4px solid #ea580c; margin-top: 10px; }
                  .footer { background-color: #1f2937; color: #9ca3af; padding: 15px; text-align: center; font-size: 12px; border-radius: 0 0 5px 5px; }
                </style>
              </head>
              <body>
                <div class="container">
                  <div class="header">
                    <h2 style="margin: 0;">New Contact Form Submission</h2>
                  </div>
                  <div class="content">
                    <div class="field">
                      <div class="label">From</div>
                      <div class="value">${name}</div>
                    </div>
                    <div class="field">
                      <div class="label">Email Address</div>
                      <div class="value"><a href="mailto:${email}" style="color: #ea580c;">${email}</a></div>
                    </div>
                    <div class="field">
                      <div class="label">Message</div>
                      <div class="message-box">${message.replace(/\n/g, '<br>')}</div>
                    </div>
                  </div>
                  <div class="footer">
                    Sent from spiritualtourstoindia.com contact form
                  </div>
                </div>
              </body>
              </html>
            `
          }]
        })
      });

      // Check SendGrid response
      if (sendGridResponse.status === 202) {
        return new Response(JSON.stringify({ 
          success: true,
          message: 'Email sent successfully'
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      } else {
        const errorText = await sendGridResponse.text();
        console.error('SendGrid error:', errorText);
        
        return new Response(JSON.stringify({ 
          success: false, 
          error: 'Failed to send email. Please try again.' 
        }), {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

    } catch (error) {
      console.error('Worker error:', error);
      
      return new Response(JSON.stringify({ 
        success: false, 
        error: 'An unexpected error occurred. Please try again.' 
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }
  }
};
