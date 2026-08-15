package com.kevinmu.gnarlywrapper

import android.annotation.SuppressLint
import android.content.ContentValues
import android.content.Context
import android.os.Bundle
import android.os.Environment
import android.os.Handler
import android.os.Looper
import android.provider.MediaStore
import android.text.InputType
import android.webkit.CookieManager
import android.webkit.URLUtil
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import java.io.InputStream
import java.io.OutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {
    
    // Define a constant key for our SharedPreferences
    private val PREFS_NAME = "GnarlyPrefs"
    private val KEY_GNARLY_URL = "gnarly_url"
    private val DEFAULT_URL = "http://gnarlypi.local"

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val webView: WebView = findViewById(R.id.gnarlyWebView)
        val settingsButton: ImageButton = findViewById(R.id.settingsButton)
        val sharedPreferences = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

        // Initialise WebView configuration
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        // ----------------------------------------------------------------------------
        // Native In-App Sandbox Downloader (Bypasses System DownloadManager)
        // ----------------------------------------------------------------------------
        webView.setDownloadListener { url, userAgent, contentDisposition, mimeType, _ ->
            val fileName = URLUtil.guessFileName(url, contentDisposition, mimeType)
            Toast.makeText(applicationContext, "Starting download: $fileName", Toast.LENGTH_SHORT).show()

            // Execute the network request on a background thread to prevent UI locking
            Executors.newSingleThreadExecutor().execute {
                try {
                    val connection = URL(url).openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.setRequestProperty("User-Agent", userAgent)
                    
                    // Inject session cookies to maintain authentication
                    val cookies = CookieManager.getInstance().getCookie(url)
                    if (cookies != null) {
                        connection.setRequestProperty("Cookie", cookies)
                    }
                    
                    connection.connect()

                    if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                        val inputStream: InputStream = connection.inputStream

                        // Utilise modern MediaStore API for API 29+ compliant scoped storage
                        val resolver = contentResolver
                        val contentValues = ContentValues().apply {
                            put(MediaStore.Downloads.DISPLAY_NAME, fileName)
                            put(MediaStore.Downloads.MIME_TYPE, mimeType)
                            // Append the custom directory to the relative path
                            put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/GnarlyPi")
                        }

                        val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, contentValues)
                        if (uri != null) {
                            val outputStream: OutputStream? = resolver.openOutputStream(uri)
                            outputStream?.use { out ->
                                // Stream the binary data directly to disk
                                inputStream.copyTo(out)
                            }
                            
                            // Post success message back to the main UI thread
                            Handler(Looper.getMainLooper()).post {
                                Toast.makeText(applicationContext, "Saved to Downloads/GnarlyPi: $fileName", Toast.LENGTH_LONG).show()
                            }
                        } else {
                            throw Exception("MediaStore rejected file creation.")
                        }
                        inputStream.close()
                    } else {
                        Handler(Looper.getMainLooper()).post {
                            Toast.makeText(applicationContext, "Download failed: HTTP ${connection.responseCode}", Toast.LENGTH_LONG).show()
                        }
                    }
                } catch (e: Exception) {
                    Handler(Looper.getMainLooper()).post {
                        Toast.makeText(applicationContext, "Download error: ${e.message}", Toast.LENGTH_LONG).show()
                    }
                }
            }
        }

        // Register the modern OnBackPressedCallback to handle hardware back navigation gracefully
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    // If the browser has history, navigate back within the web view
                    webView.goBack()
                } else {
                    // If no history remains, temporarily disable this callback and let the OS close the app
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                    // Re-enable just in case the activity is resumed from the background
                    isEnabled = true
                }
            }
        })

        // Fetch the saved URL from disk, or use the default if it doesn't exist yet
        val savedUrl = sharedPreferences.getString(KEY_GNARLY_URL, DEFAULT_URL) ?: DEFAULT_URL
        webView.loadUrl(savedUrl)

        // Attach listener to our configuration button
        settingsButton.setOnClickListener {
            showConfigurationDialog(webView)
        }
    }

    private fun showConfigurationDialog(webView: WebView) {
        val sharedPreferences = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val currentUrl = sharedPreferences.getString(KEY_GNARLY_URL, DEFAULT_URL)

        val builder = AlertDialog.Builder(this)
        builder.setTitle("Target Address")
        builder.setMessage("Enter the IP address or hostname of the GnarlyPi.")

        // Set up the text input field
        val input = EditText(this)
        input.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_URI
        input.setText(currentUrl)
        
        // Add padding to the input for better touch UI
        input.setPadding(48, 32, 48, 32)
        builder.setView(input)

        builder.setPositiveButton("Save & Connect") { dialog, _ ->
            var newUrl = input.text.toString().trim()
            
            if (newUrl.isNotEmpty()) {
                // Ensure the HTTP protocol is present to satisfy Android's cleartext routing
                if (!newUrl.startsWith("http://") && !newUrl.startsWith("https://")) {
                    newUrl = "http://$newUrl"
                }
                
                // Save the new target to disk
                sharedPreferences.edit().putString(KEY_GNARLY_URL, newUrl).apply()
                
                // Immediately route the WebView to the new address
                webView.loadUrl(newUrl)
            }
            dialog.dismiss()
        }

        builder.setNegativeButton("Cancel") { dialog, _ ->
            dialog.cancel()
        }

        builder.show()
    }
}