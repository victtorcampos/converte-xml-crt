# Development Roadmap: XML NFe Converter

This document outlines the development plan and checklist for creating the XML NFe Converter application.

## Phase 1: Core Conversion Logic (Backend)

The primary focus of this phase is to build the fundamental engine for XML conversion.

- **Tasks:**
  - **XML Parsing and Validation (RF01):** Implement a module to parse, validate, and handle errors for uploaded `.xml` files.
  - **Conversion Engine (RF02):** Develop the core logic to map CSOSN to CST, implement transformation rules, and make the engine configurable.
  - **Recalculation of Totals (RF03):** Create a function to iterate through converted items and recalculate values in the `<ICMSTot>` block.
  - **CRT Update (RF04):** Implement logic to update the `<CRT>` field in the `<emit>` group.
  - **Unit Testing:** Write a comprehensive suite of unit tests for all conversion functions to ensure accuracy and reliability.

## Phase 2: FastAPI Application & API Endpoints

This phase involves setting up the web server and exposing the core logic through API endpoints.

- **Tasks:**
  - **FastAPI Project Setup:** Initialize a new FastAPI project with a logical structure.
  - **File Upload Endpoint (RF01, RF05):** Create an API endpoint (`/`) to handle multiple file uploads and validation.
  - **Processing Endpoint:** Create a main endpoint that orchestrates the entire conversion process.
  - **Error Handling (RF07):** Implement application-level error handling for fatal and non-fatal errors.

## Phase 3: Frontend User Interface

This phase focuses on building a simple and effective user interface.

- **Tasks:**
  - **HTML Structure (RF05):** Create the basic HTML for the upload page.
  - **Styling with Tailwind CSS:** Apply Tailwind CSS to create a clean and modern user interface.
  - **Dynamic Interactivity with HTMX:** Use HTMX to handle file uploads without a full page reload.
  - **WebSocket Integration:** Initially planned, but descoped to simplify the final solution.

## Phase 4: Output Generation and Reporting

This phase deals with creating the final downloadable package for the user.

- **Tasks:**
  - **ZIP File Generation (RF06):** Implement logic to create a `.zip` archive with `convertidos/` and `erros/` subdirectories.
  - **Report Generation (RF06):** Dynamically generate `relatorio.txt` and include the static `aviso_legal.txt`.
  - **Download Endpoint (RF05):** Create an API endpoint to serve the generated `.zip` file.

## Phase 5: Finalization and Deployment

This final phase involves polishing the application, ensuring it's secure, and preparing it for deployment.

- **Tasks:**
  - **Security Hardening (RNF02):** Implement security measures, including file extension validation and sanitizing filenames.
  - **Performance Optimization (RNF01):** Profile and optimize the application.
  - **Final Testing and Bug Fixing:** Conduct end-to-end testing and address any remaining bugs.
  - **Deployment Preparation:** Create deployment scripts (`devserver.sh`, `devserver.ps1`) and document the process (`README.md`).

# Development Checklist

- [x] **Phase 1: Core Conversion Logic**
    - [x] **RF01: XML Validation**
        - [x] Parse XML and check if it's well-formed.
        - [x] Validate NFe namespace.
        - [x] Check for `<nfeProc>` or `<NFe>` root tag.
        - [x] Validate `<mod>` is 55 or 65.
        - [x] Validate `<CRT>` is 1.
    - [x] **RF02: Conversion Engine**
        - [x] Implement CSOSN to CST mapping table.
        - [x] Implement conversion rules for CST=00.
        - [x] Implement conversion rules for CST=41.
        - [x] Implement conversion rules for CST=60.
        - [x] Handle CSOSN 900.
    - [x] **RF03: Recalculate Totals**
        - [x] Sum `vBC`, `vICMS` from item details.
        - [x] Update the `<ICMSTot>` group.
    - [x] **RF04: Update CRT**
        - [x] Update the `<CRT>` field in the `<emit>` group.
    - [x] **Unit Tests**
        - [x] Write unit tests for all core conversion functions.
- [x] **Phase 2: FastAPI Application**
    - [x] Set up basic FastAPI app.
    - [x] Create `/` endpoint for upload and processing.
    - [x] Implement fatal and non-fatal error handling.
- [x] **Phase 3: Frontend and User Interface**
    - [x] Create `index.html`.
    - [x] Add Tailwind CSS.
    - [x] Implement file upload with HTMX.
    - [ ] Implement real-time progress with WebSockets (Descoped).
- [x] **Phase 4: Output and Reporting**
    - [x] Implement ZIP file creation.
    - [x] Generate `relatorio.txt`.
    - [x] Generate `aviso_legal.txt`.
    - [x] Create download response.
- [x] **Phase 5: Finalization and Deployment**
    - [x] Implement security best practices.
    - [ ] Perform formal load testing (RNF01).
    - [x] Code review and refactoring.
    - [x] Prepare deployment scripts and documentation.
