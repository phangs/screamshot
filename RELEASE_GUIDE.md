# Mosaic Release Guide

This document outlines the step-by-step procedure to compile, optimize, package, and distribute highly optimized production releases of **Mosaic** on Linux systems.

---

## 📋 Prerequisites & Dependencies

To build a production-ready release, ensure that the necessary build systems and system libraries are installed on the host machine.

### On Debian/Ubuntu-based Systems:
```bash
sudo apt update
sudo apt install -y build-essential pkg-config libgtk-3-dev libx11-dev libxtst-dev libwayland-dev libxkbcommon-dev
```

### On Fedora/RedHat-based Systems:
```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install -y pkg-config gtk3-devel libX11-devel libXtst-devel wayland-devel libxkbcommon-devel
```

### On Arch Linux:
```bash
sudo pacman -Syu --needed base-devel pkgconf gtk3 libxtst wayland libxkbcommon
```

---

## 🚀 Building the Release Binary

To generate the most performant, optimized, and stripped executable, execute the following commands in the project root:

### 1. Compile in Release Mode
Run the compiler with high-optimization flags:
```bash
cargo build --release
```
> [!NOTE]
> The compiled binary will be placed at `target/release/mosaic`.

### 2. Strip Debug Symbols (Highly Recommended)
Rust release builds still contain substantial debugging symbols. Stripping them reduces the binary footprint significantly (typically from **~40MB down to ~3MB**):
```bash
strip target/release/mosaic
```

### 3. Verification
Verify the build is fully operational:
```bash
./target/release/mosaic
```

---

## 📦 Packaging & Installation (Linux Desktop Integration)

To integrate `mosaic` natively into your Linux desktop environment, follow these steps to install the executable, set up launcher icons, and configure keybindings.

### 1. Install the Executable
Move the stripped executable to a standard user bin path:
```bash
sudo cp target/release/mosaic /usr/local/bin/
```

### 2. Install Desktop Launcher
Create a beautiful desktop launcher file so you can search and start `mosaic` from your application menu.

Create `/usr/share/applications/mosaic.desktop` (System-wide) or `~/.local/share/applications/mosaic.desktop` (User-specific):

```ini
[Desktop Entry]
Name=Mosaic
Comment=Premium scrolling and region screenshot utility
Exec=/usr/local/bin/mosaic
Icon=screenshot
Terminal=false
Type=Application
Categories=Utility;Graphics;
StartupNotify=true
```

Update desktop database to register the entry:
```bash
update-desktop-database ~/.local/share/applications/
```

### 3. Autostart Integration
`mosaic` is designed to run silently in the system tray. To launch it automatically upon desktop login, copy the desktop entry to your autostart directory:
```bash
mkdir -p ~/.config/autostart
cp ~/.local/share/applications/mosaic.desktop ~/.config/autostart/
```

---

## 🛠 Troubleshooting & Optimization Flags

If you want to squeeze even more performance or compile for minimal binary sizes, you can customize the compilation profile in `Cargo.toml`.

Add the following to your `Cargo.toml` if it isn't already present:

```toml
[profile.release]
opt-level = 3          # Maximize speed/performance optimizations
lto = true             # Enable Link-Time Optimization across all crates
codegen-units = 1      # Reduce parallel codegen units to improve LTO optimization
panic = "abort"        # Eliminate stack unwinding tables for smaller binary footprint
strip = true           # Automatically strip symbols during build (requires Rust 1.59+)
```

---

## 🤖 GitHub Actions Automated Release Workflow

Mosaic has a GitHub Actions CI/CD workflow configured at `.github/workflows/release.yml` that automatically builds, strips, packages, and drafts a new release with assets for **Linux (x64)**, **Windows (x64)**, **macOS Intel (x64)**, and **macOS Apple Silicon (arm64)**!

Here are the exact Git commands to trigger a new automated release:

### 1. Update the Version in `Cargo.toml`
Open `Cargo.toml` and increment the version (e.g., `version = "0.2.0"`). Commit the version change:
```bash
git add Cargo.toml
git commit -m "bump: version 0.2.0"
git push origin main
```

### 2. Create and Tag the Release
Create a new annotated Git tag matching the `v*` wildcard pattern (e.g., `v0.2.0`):
```bash
git tag -a v0.2.0 -m "Release v0.2.0"
```

### 3. Push the Tag to GitHub
Pushing the tag triggers the automated release builder immediately:
```bash
git push origin v0.2.0
```

> [!TIP]
> **Manual Build Option**: If you just want to compile the binaries without making a formal release, navigate to the **Actions** tab on your GitHub repository page, click the **Release** workflow in the left sidebar, and click the **Run workflow** dropdown button.
