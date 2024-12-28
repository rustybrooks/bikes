import { rem, Stack, Tooltip, UnstyledButton, useMantineColorScheme } from '@mantine/core';
import { useLocation, useNavigate } from 'react-router-dom';
import classes from './NavBar.module.css';
import { icons } from '../constants/icons';

interface NavbarLinkProps {
  icon: typeof icons.search;
  label: string;
  active?: boolean;

  onClick?(): void;
}

function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
  return (
    <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
      <UnstyledButton onClick={onClick} className={classes.link} data-active={active || undefined}>
        <Icon style={{ width: rem(30), height: rem(30) }} stroke={1.5} />
      </UnstyledButton>
    </Tooltip>
  );
}

const menuItems = [
  { icon: icons.calendar, label: 'Calendar', url: '/' },
  { icon: icons.training, label: 'Training Plan', url: '/training' },
  { icon: icons.graph, label: 'Graphs', url: '/graphs' },
];

const isAuthenticated = true;

export const NavBar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();

  const modeClickHandler = () => {
    toggleColorScheme();
    const invertedColorScheme = colorScheme === 'dark' ? 'light' : '~adrk';
    localStorage.setItem('color-scheme', invertedColorScheme);
  };

  const links = menuItems.map(link => (
    <NavbarLink {...link} key={link.label} active={location.pathname === link.url} onClick={() => navigate(link.url)} />
  ));

  return (
    <nav className={classes.navbar}>
      <div className={classes.navbarMain}>
        <Stack justify="center" gap={0}>
          {links}
        </Stack>
      </div>

      <Stack justify="center" gap={0}>
        {isAuthenticated ? (
          <>
            <NavbarLink icon={icons.user} label="User" onClick={() => navigate('/')} />
            <NavbarLink icon={icons.logout} label="Logout" onClick={() => {}} />
          </>
        ) : (
          <>
            <NavbarLink icon={icons.login} label="Login" onClick={() => {}} />
          </>
        )}
        <NavbarLink icon={icons.colorMode} label={'Swap Mode'} onClick={modeClickHandler} />
      </Stack>
    </nav>
  );
};
