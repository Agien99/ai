function Brand({
  compact = false,
}) {
  return (
    <div
      className={
        compact
          ? "brand brand-compact"
          : "brand"
      }
    >
      <img
        src={
          `${import.meta.env.BASE_URL}` +
          "logo_main.png"
        }
        alt="RouletteIQ"
        className="brand-logo"
      />
    </div>
  );
}


export default Brand;