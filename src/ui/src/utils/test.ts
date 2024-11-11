type Order = { id: number; amount: number; price: number };

const myFunction = (order: Order): Promise<boolean> => {
  const orderEntries = Object.entries(order);
  const orderWithTotal = [...orderEntries, ['total', order.amount * order.price]];
  const newOrder = Object.fromEntries(orderWithTotal);
  return newOrder;
};

const x = await myFunction({ id: 1, amount: 1, price: 1 });
console.log(x);
