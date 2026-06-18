//
//  LoginViewPage.swift
//  Page Object for LoginView
//

import XCTest

class LoginViewPage {
    
    let app: XCUIApplication
    
    init(app: XCUIApplication) {
        self.app = app
    }
    
    // MARK: - Elements

    var person_circle_fill: XCUIElement {
        return app.images["person.circle.fill"]
    }

    var Welcome_Back: XCUIElement {
        return app.staticTexts["Welcome Back"]
    }

    var Username: XCUIElement {
        return app.textFields["Username"]
    }

    var Password: XCUIElement {
        return app.secureTextFields["Password"]
    }

    var Remember_Me: XCUIElement {
        return app.switches["Remember Me"]
    }

    var Login: XCUIElement {
        return app.staticTexts["Login"]
    }

    var Forgot_Password: XCUIElement {
        return app.buttons["Forgot Password?"]
    }

    var Don: XCUIElement {
        return app.staticTexts["Don"]
    }

    var Sign_Up: XCUIElement {
        return app.staticTexts["Sign Up"]
    }

    var OK: XCUIElement {
        return app.buttons["OK"]
    }

    var Invalid_username_or_password: XCUIElement {
        return app.staticTexts["Invalid username or password"]
    }

    var Sign_Up_View: XCUIElement {
        return app.staticTexts["Sign Up View"]
    }

    
    // MARK: - Actions
    
    func waitForView() -> Bool {
        return app.navigationBars["LoginView"].waitForExistence(timeout: 5)
    }
}
