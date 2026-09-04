import {
  getNumberType,
} from "../../utils/roulette";

function RouletteNumber({
  number,
  size = "normal",
}) {
  const type =
    getNumberType(number);

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

export default RouletteNumber;