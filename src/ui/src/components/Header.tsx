import { Button, Modal } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Login } from './Login';

export const Header = () => {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Button onClick={open}>Open modal</Button>
      <Modal opened={opened} onClose={close} size="lg" title="Login">
        <Login />
      </Modal>
    </>
  );
};
