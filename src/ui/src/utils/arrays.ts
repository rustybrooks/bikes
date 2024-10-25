export const chunkArray = <T>(arr: T[], chunkSize: number): T[][] => {
  const result = [];

  for (let i = 0; i < arr.length; i += chunkSize) {
    const chunk = arr.slice(i, i + chunkSize);
    result.push(chunk);
  }

  return result;
};
