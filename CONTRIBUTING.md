# Contributing to JSONly

Thank you for considering contributing to **JSONly**! We welcome contributions from the community. By following these guidelines, you'll help ensure that contributions are smooth and beneficial for everyone involved.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Code](#submitting-code)
- [Development Setup](#development-setup)
- [Style Guide](#style-guide)
- [Testing](#testing)
- [License](#license)

---

### Code of Conduct

We’re committed to creating a welcoming and respectful environment for everyone. All contributors are expected to:

- Be kind and constructive in all communications.

- Respect differing opinions and experiences.

- Avoid personal attacks, harassment, and discriminatory language.

By participating in this project, you agree to uphold these standards. Let's keep it friendly and collaborative.

---

### How to Contribute

#### Reporting Bugs

If you encounter a bug, please check the [issues](https://github.com/DudenessBoy/JSONly/issues) to see if it has already been reported. If not, you can report it by opening a new issue.

- Provide a **clear description** of the issue.
- Include steps to **reproduce** the problem.
- Specify the **version** of JSONly you're using.
- Attach any **error messages** or logs, if applicable.

#### Suggesting Features

We welcome suggestions for new features or improvements! If you have an idea, feel free to open a new issue with the label "Feature Request".

- Explain the **problem** the feature would solve.
- Describe how the feature would work, including any UI or UX ideas if applicable.
- Keep the feature aligned with the vision of JSONly, focusing on enhancing the usability of the app.

#### Submitting Code

We are happy to accept code contributions! Here's how to get started:

1. **Fork** the repository and clone it to your machine.
2. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b my-feature-branch
   ```
3. **Make your changes**, following the style guide below.
4. **Test your changes** to ensure everything works as expected.
5. **Commit** your changes with a clear, descriptive message:
   ```bash
   git commit -m "Fix bug with feature X"
   ```
6. **Push** your changes to your forked repository:
   ```bash
   git push origin my-feature-branch
   ```
7. **Create a pull request** to the main repository. Be sure to explain what your changes do and why they are necessary.

---

### Development Setup

To contribute code, you'll need to set up the development environment.

1. Clone the repository:
   ```bash
   git clone https://github.com/DudenessBoy/JSONly.git
   cd JSONly
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

For detailed setup instructions, refer to the [README.md](README.md).

---

### Style Guide

To maintain consistency across the codebase, please follow these style guidelines:

- **Python Code**: Stick to [PEP 8](https://peps.python.org/pep-0008/).
- **Naming**: Use camelCase for variable names and function names
- **Comments**: Add meaningful comments explaining **why** something is done, not just **what** is done.
- **Commit Messages**: Use clear, descriptive commit messages. Start with a short summary of the change, followed by a detailed explanation if necessary.
  
Example:
```bash
Fix crash while opening settings

The app crashed when the settings panel was opened. Fixed some faulty code causing the crash.
```

---

### Testing

Before submitting a pull request, make sure your changes are properly tested.

---

#### Contributing Translations

Want to help make **JSONly** accessible to more people around the world? You can contribute translations or improve existing ones!

Here’s how to get started:

1. **Check for existing language files**  
   Translation files are located in the `lang/` directory. They are named using standard language codes (e.g., `en.json`, `fr.json`, `es.json`).

2. **Add a new translation**  
   If your language is missing:
   - Create a new file with the appropriate language code (e.g., `de.json` for German).
   - Copy the structure from `en.json` and translate the values, **not the keys**.
   - Make sure the file is valid JSON. You can even preview it using JSONly if you want.

3. **Update an existing translation**  
   - Open the existing language file.
   - Translate any missing or outdated strings.
   - Keep formatting and keys consistent.

4. **Test your translation**  
   - Launch JSONly and switch to your language from the settings menu.
   - Make sure your changes appear correctly and don't break layout or functionality.

5. **Submit your translation**  
   - Follow the [Submitting Code](#submitting-code) instructions.
   - In your pull request, mention which language you worked on and whether it’s a new addition or an update.

Tips:
- Avoid machine translation unless you're verifying it manually.
- Keep translations concise and user-friendly.
- If you're unsure about a phrasing, feel free to ask in the issue tracker or discussions.

### License

By contributing to **JSONly**, you agree that your contributions will be licensed under the [MIT License](LICENSE).