# Maintainer: fridge24 <https://github.com/fridge24/hyprbinds>

pkgname=hyprbinds
pkgver=1.0.0
pkgrel=1
pkgdesc="Hyprbinds, a PyQt6 gui application for modifiying keybinds within Hyprland"
arch=('x86_64')
url="https://github.com/fridge24/hyprbinds"
license=('MIT') 
depends=('python' 'python-pyqt6')
source=("https://github.com/fridge24/hyprbinds/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Replace with actual checksum

package() {
    install -Dm755 "$srcdir/$pkgname-$pkgver/src/main.py" "$pkgdir/usr/bin/$pkgname"
    install -Dm644 "$srcdir/$pkgname-$pkgver/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    install -Dm755 "$srcdir/$pkgname-$pkgver/scripts/hyprbinds" "$pkgdir/usr/bin/$pkgname"
}
