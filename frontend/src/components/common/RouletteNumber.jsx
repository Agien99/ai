function getNumberType(number) {
  if (number === 0) {
    return "green";
  }

  const redNumbers = [
    1, 3, 5, 7, 9,
    12, 14, 16, 18,
    19, 21, 23, 25, 27,
    30, 32, 34, 36,
  ];

  return redNumbers.includes(number)
    ? "red"
    : "black";
}

function RouletteNumber({
  number,
  size = "normal",
}) {
  const type = getNumberType(number);

  return (
    <span
      className={
        `roulette-number roulette-number-${type} ` +
        `roulette-number-${size}`
      }
    >
      {number}
    </span>
  );
}

export {
  getNumberType,
};

export default RouletteNumber;