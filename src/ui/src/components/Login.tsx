import { Button, Container, Paper, PasswordInput, TextInput, Title } from '@mantine/core';
import { useContext, useState } from 'react';
import { NavigateFunction, useNavigate } from 'react-router';
import { FrameworkContext } from '../contexts/FrameworkContext';

const login = async (navigate: NavigateFunction, frameworks: any, username: string, password: string): Promise<string> => {
  try {
    const resp = await frameworks.data.Users.login({ username, password });
    if (resp.status === 403) {
      return resp.details.detail;
    }
    navigate('/');
  } catch (error) {
    console.log(error);
    return error as string;
  }

  return '';
};

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { frameworks } = useContext(FrameworkContext);
  const navigate = useNavigate();

  return (
    <Container size={420} my={40}>
      <Title ta="center">Welcome back!</Title>
      {/* <Text c="dimmed" size="sm" ta="center" mt={5}> */}
      {/*  Do not have an account yet?{' '} */}
      {/*  <Anchor size="sm" component="button"> */}
      {/*    Create account */}
      {/*  </Anchor> */}
      {/* </Text> */}

      <Paper withBorder shadow="md" p={30} mt={30} radius="md">
        <TextInput error={error} value={username} label="Username" required onChange={event => setUsername(event.currentTarget.value)} />
        <PasswordInput
          value={password}
          label="Password"
          placeholder="Your password"
          required
          mt="md"
          onChange={event => setPassword(event.currentTarget.value)}
        />
        <Button fullWidth mt="xl" onClick={async () => setError(await login(navigate, frameworks, username, password))}>
          Sign in
        </Button>
      </Paper>
    </Container>
  );
};
