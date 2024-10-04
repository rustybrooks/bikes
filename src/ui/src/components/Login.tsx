import { Button, Container, Paper, PasswordInput, Tabs, TextInput, Title } from '@mantine/core';
import { useContext, useState } from 'react';
import { NavigateFunction, useNavigate } from 'react-router';
import { apiFetch, apiUrl } from '../api/api-fetch.ts';

const login = async (navigate: NavigateFunction, username: string, password: string): Promise<string> => {
  try {
    const resp = await apiFetch(apiUrl('USERS_LOGIN'), {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
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

const signup = async (navigate: NavigateFunction, username: string, password: string, password2: string): Promise<string> => {
  try {
    const resp = await apiFetch(apiUrl('USERS_SIGNUP'), {
      method: 'POST',
      body: JSON.stringify({ username, password, password2 }),
    });
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
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  return (
    <Container size={420} my={40}>
      <Tabs defaultValue="login">
        <Tabs.List>
          <Tabs.Tab value="login">Login</Tabs.Tab>
          <Tabs.Tab value="signup">Signup</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="login">
          <Title ta="center">Welcome back!</Title>
          <Paper withBorder shadow="md" p={30} mt={30} radius="md">
            <TextInput
              error={error}
              value={username}
              label="Username"
              required
              onChange={event => setUsername(event.currentTarget.value)}
            />
            <PasswordInput
              value={password}
              label="Password"
              placeholder="Your password"
              required
              mt="md"
              onChange={event => setPassword(event.currentTarget.value)}
            />
            <Button fullWidth mt="xl" onClick={async () => setError(await login(navigate, username, password))}>
              Sign in
            </Button>
          </Paper>
        </Tabs.Panel>

        <Tabs.Panel value="signup">
          <Title ta="center">Sign up</Title>
          <Paper withBorder shadow="md" p={30} mt={30} radius="md">
            <TextInput
              error={error}
              value={username}
              label="Username"
              required
              onChange={event => setUsername(event.currentTarget.value)}
            />
            <PasswordInput
              value={password}
              label="Password"
              placeholder="Your password"
              required
              mt="md"
              onChange={event => setPassword(event.currentTarget.value)}
            />
            <PasswordInput
              value={password2}
              label="Password (again)"
              placeholder="Your password"
              required
              mt="md"
              onChange={event => setPassword2(event.currentTarget.value)}
            />
            <Button fullWidth mt="xl" onClick={async () => setError(await signup(navigate, username, password, password2))}>
              Sign up
            </Button>
          </Paper>
        </Tabs.Panel>
      </Tabs>
    </Container>
  );
};
