from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "images"
OUTPUT_ROOT = IMAGE_ROOT / "optimized"

SOURCE_GROUPS = [
    IMAGE_ROOT / "ux-portfolio",
    IMAGE_ROOT / "LanMao截图",
]

SINGLE_IMAGES = [
    ROOT / "语言学习研究效果图.png",
    IMAGE_ROOT / "hero-photo-个人照片-半身照.jpg",
    IMAGE_ROOT / "project-01-智能眼镜语言学习系统-AR眼镜界面封面.jpg",
    IMAGE_ROOT / "project-02-发散型交互体验设计-封面.jpg",
    IMAGE_ROOT / "project-03-LanmaoAssist-房源管理系统封面.jpg",
    IMAGE_ROOT / "poster-detail.jpg",
]


def save_webp(source: Path, destination: Path, max_width: int, quality: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.Resampling.LANCZOS)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        image.save(destination, "WEBP", quality=quality, method=6)


def output_path(source: Path, thumbnail: bool = False) -> Path:
    try:
        relative = source.relative_to(IMAGE_ROOT)
    except ValueError:
        relative = Path("site") / source.name
    prefix = OUTPUT_ROOT / ("thumbs" if thumbnail else "full")
    return (prefix / relative).with_suffix(".webp")


def main() -> None:
    sources = list(SINGLE_IMAGES)
    for group in SOURCE_GROUPS:
        sources.extend(
            path for path in group.rglob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
        )

    original_bytes = 0
    optimized_bytes = 0
    for source in sources:
        original_bytes += source.stat().st_size
        full = output_path(source)
        save_webp(source, full, max_width=2000, quality=82)
        optimized_bytes += full.stat().st_size

        if "ux-portfolio" in source.parts:
            thumb = output_path(source, thumbnail=True)
            save_webp(source, thumb, max_width=280, quality=68)
            optimized_bytes += thumb.stat().st_size

    print(f"Optimized {len(sources)} images")
    print(f"Original: {original_bytes / 1024 / 1024:.2f} MB")
    print(f"Generated full and thumbnail assets: {optimized_bytes / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
