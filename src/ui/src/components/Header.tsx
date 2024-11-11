import { Button } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Login } from './Login';
import { FixedModal } from './FixedModal';

export const Header = () => {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Button onClick={open}>Open modal</Button>
      <FixedModal opened={opened} onClose={close} size="lg" title="Login">
        <Login />
      </FixedModal>
    </>
  );
};
