//
//  LoginView.swift
//  Sample SwiftUI App
//
//  Example login view for testing XCUI test generation
//

import SwiftUI

struct LoginView: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var rememberMe: Bool = false
    @State private var showingAlert: Bool = false
    @State private var isLoading: Bool = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Logo
                Image(systemName: "person.circle.fill")
                    .resizable()
                    .frame(width: 100, height: 100)
                    .foregroundColor(.blue)
                    .accessibilityIdentifier("loginLogo")
                
                // Title
                Text("Welcome Back")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .accessibilityIdentifier("welcomeTitle")
                
                // Username field
                TextField("Username", text: $username)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .autocapitalization(.none)
                    .accessibilityIdentifier("usernameField")
                
                // Password field
                SecureField("Password", text: $password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .accessibilityIdentifier("passwordField")
                
                // Remember me toggle
                Toggle("Remember Me", isOn: $rememberMe)
                    .accessibilityIdentifier("rememberMeToggle")
                
                // Login button
                Button(action: {
                    login()
                }) {
                    if isLoading {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    } else {
                        Text("Login")
                            .fontWeight(.semibold)
                    }
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
                .disabled(username.isEmpty || password.isEmpty || isLoading)
                .accessibilityIdentifier("loginButton")
                
                // Forgot password link
                Button("Forgot Password?") {
                    // Navigate to forgot password
                }
                .accessibilityIdentifier("forgotPasswordButton")
                
                Spacer()
                
                // Sign up link
                HStack {
                    Text("Don't have an account?")
                    NavigationLink(destination: SignUpView()) {
                        Text("Sign Up")
                            .fontWeight(.semibold)
                    }
                    .accessibilityIdentifier("signUpLink")
                }
            }
            .padding()
            .navigationTitle("Login")
            .alert("Login Failed", isPresented: $showingAlert) {
                Button("OK", role: .cancel) { }
            } message: {
                Text("Invalid username or password")
            }
        }
    }
    
    private func login() {
        isLoading = true
        
        // Simulate network call
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            isLoading = false
            
            // Simple validation
            if username == "test" && password == "password" {
                // Navigate to home
            } else {
                showingAlert = true
            }
        }
    }
}

struct SignUpView: View {
    var body: some View {
        Text("Sign Up View")
            .navigationTitle("Sign Up")
    }
}

#Preview {
    LoginView()
}

// Made with Bob
