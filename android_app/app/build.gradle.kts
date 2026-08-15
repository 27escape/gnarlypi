import java.util.Properties
import java.io.FileInputStream

plugins {
    // AGP 9+ automatically provisions the Kotlin plugin in the background
    alias(libs.plugins.android.application)
}

// ----------------------------------------------------------------------------
// Headless Deployment: Dynamic Credential Injection
// ----------------------------------------------------------------------------
// Load the secure credentials from local.properties to protect cryptographic keys from version control
val keystoreProperties = Properties()
val localPropertiesFile = rootProject.file("local.properties")
if (localPropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(localPropertiesFile))
}

android {
    namespace = "com.kevinmu.gnarlywrapper"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.kevinmu.gnarlywrapper"
        minSdk = 31
        targetSdk = 34

        // INCREMENT THESE FOR EVERY NEW DEPLOYMENT
        versionCode = 4
        versionName = "1.4"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    // Define the release signing configuration dynamically
    signingConfigs {
        create("release") {
            // Anchor the keystore file search to the root project directory
            storeFile = rootProject.file(keystoreProperties.getProperty("KEYSTORE_FILE") ?: "gnarly_keystore.jks")
            keyAlias = keystoreProperties.getProperty("KEY_ALIAS")
            storePassword = keystoreProperties.getProperty("KEYSTORE_PASSWORD")
            keyPassword = keystoreProperties.getProperty("KEY_PASSWORD")
        }
    }

    buildTypes {
        release {
            // Command the release build to utilise the secure config defined above
            signingConfig = signingConfigs.getByName("release")

            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    // Standard UI and architectural libraries required for your Edge-to-Edge configuration
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.constraintlayout)

    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}