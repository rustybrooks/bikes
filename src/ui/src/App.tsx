import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/charts/styles.css';
import { Route, Routes } from 'react-router';
import { AppShell, createTheme, MantineProvider, rem } from '@mantine/core';
import { Header } from './components/Header';
import { NavBar } from './components/NavBar';
import { TrainingPlans } from './views/TrainingPlans';
import { TrainingPlansManage } from './views/TrainingPlansManage';
import { StravaCallback } from './views/StravaCallback';
import { Home } from './views/Home';
import { Activity } from './views/Activity';
import { Graphs } from './views/Graphs';

const theme = createTheme({
  //
  // /** Controls focus ring styles. Supports the following options:
  //  *  - `auto` – focus ring is displayed only when the user navigates with keyboard (default value)
  //  *  - `always` – focus ring is displayed when the user navigates with keyboard and mouse
  //  *  - `never` – focus ring is always hidden (not recommended)
  //  */
  // focusRing: 'auto' | 'always' | 'never';
  //
  // /** rem units scale, change if you customize font-size of `<html />` element
  //  *  default value is `1` (for `100%`/`16px` font-size on `<html />`)
  //  */
  scale: 1,
  //
  // /** Determines whether `font-smoothing` property should be set on the body, `true` by default */
  fontSmoothing: true,
  //
  // /** White color */
  white: '#ffffff',
  //
  // /** Black color */
  black: '#402000',
  //
  // /** Object of colors, key is color name, value is an array of at least 10 strings (colors) */
  // There is supposed to be 10 variants per color, these are just copies

  //
  // /** Index of theme.colors[color].
  //  *  Primary shade is used in all components to determine which color from theme.colors[color] should be used.
  //  *  Can be either a number (0–9) or an object to specify different color shades for light and dark color schemes.
  //  *  Default value `{ light: 6, dark: 8 }`
  //  *
  //  *  For example,
  //  *  { primaryShade: 6 } // shade 6 is used both for dark and light color schemes
  //  *  { primaryShade: { light: 6, dark: 7 } } // different shades for dark and light color schemes
  //  * */
  // primaryShade: 1,
  //
  // /** Key of `theme.colors`, hex/rgb/hsl values are not supported.
  //  *  Determines which color will be used in all components by default.
  //  *  Default value – `blue`.
  //  * */
  // primaryColor: "dm-green",
  //
  // /** Function to resolve colors based on variant.
  //  *  Can be used to deeply customize how colors are applied to `Button`, `ActionIcon`, `ThemeIcon`
  //  *  and other components that use colors from theme.
  //  * */
  // variantColorResolver: VariantColorsResolver;
  //
  // /** Determines whether text color must be changed based on the given `color` prop in filled variant
  //  *  For example, if you pass `color="blue.1"` to Button component, text color will be changed to `var(--mantine-color-black)`
  //  *  Default value – `false`
  //  * */
  // autoContrast: boolean;
  //
  // /** Determines which luminance value is used to determine if text color should be light or dark.
  //  *  Used only if `theme.autoContrast` is set to `true`.
  //  *  Default value is `0.3`
  //  * */
  // luminanceThreshold: number;
  //
  // /** font-family used in all components, system fonts by default */
  fontFamily: 'Red Hat Display',
  //
  // /** Monospace font-family, used in code and other similar components, system fonts by default  */
  fontFamilyMonospace: 'Red Hat Mono',
  //
  // /** Controls various styles of h1-h6 elements, used in TypographyStylesProvider and Title components */
  headings: {
    fontFamily: 'Oxanium',
    // fontWeight: string;
    // textWrap: 'wrap' | 'nowrap' | 'balance' | 'pretty' | 'stable';
    // sizes: {
    //     h1: HeadingStyle;
    //     h2: HeadingStyle;
    //     h3: HeadingStyle;
    //     h4: HeadingStyle;
    //     h5: HeadingStyle;
    //     h6: HeadingStyle;
    // };
  },
  //
  // /** Object of values that are used to set `border-radius` in all components that support it */
  // radius: MantineRadiusValues;
  //
  // /** Key of `theme.radius` or any valid CSS value. Default `border-radius` used by most components */
  // defaultRadius: MantineRadius;
  //
  // /** Object of values that are used to set various CSS properties that control spacing between elements */
  // spacing: MantineSpacingValues;
  //
  // /** Object of values that are used to control `font-size` property in all components */
  // fontSizes: MantineFontSizesValues;
  //
  // /** Object of values that are used to control `line-height` property in `Text` component */
  // lineHeights: MantineLineHeightValues;
  //
  // /** Object of values that are used to control breakpoints in all components,
  //  *  values are expected to be defined in em
  //  * */
  // breakpoints: MantineBreakpointsValues;
  //
  // /** Object of values that are used to add `box-shadow` styles to components that support `shadow` prop */
  // shadows: MantineShadowsValues;
  //
  // /** Determines whether user OS settings to reduce motion should be respected, `false` by default */
  // respectReducedMotion: boolean;
  //
  // /** Determines which cursor type will be used for interactive elements
  //  * - `default` – cursor that is used by native HTML elements, for example, `input[type="checkbox"]` has `cursor: default` styles
  //  * - `pointer` – sets `cursor: pointer` on interactive elements that do not have these styles by default
  //  */
  // cursorType: 'default' | 'pointer';
  //
  // /** Default gradient configuration for components that support `variant="gradient"` */
  // defaultGradient: MantineGradient;
  //
  // /** Class added to the elements that have active styles, for example, `Button` and `ActionIcon` */
  // activeClassName: string;
  //
  // /** Class added to the elements that have focus styles, for example, `Button` or `ActionIcon`.
  //  *  Overrides `theme.focusRing` property.
  //  */
  // focusClassName: string;
  //
  // /** Allows adding `classNames`, `styles` and `defaultProps` to any component */
  // components: MantineThemeComponents;
  //
  // /** Any other properties that you want to access with the theme objects */
  // other: MantineThemeOther;
});

const NoMatch = () => {
  return <div>(No Match)</div>;
};

export const App = () => {
  return (
    <MantineProvider defaultColorScheme="auto" theme={theme}>
      <AppShell
        withBorder={false}
        padding="md"
        header={{ height: '50px', offset: true }}
        footer={{ height: 0 }}
        navbar={{
          width: rem('80px'),
          breakpoint: 'sm',
        }}
      >
        <AppShell.Header>
          <Header />
        </AppShell.Header>
        <AppShell.Navbar p="md">
          <NavBar />
        </AppShell.Navbar>
        <AppShell.Main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/training" element={<TrainingPlans />} />
            <Route path="/activity/:id" element={<Activity />} />
            <Route path="/training/manage" element={<TrainingPlansManage />} />
            <Route path="/training/manage/:command" element={<TrainingPlansManage />} />
            <Route path="/graphs" element={<Graphs />} />
            <Route path="/strava_callback" element={<StravaCallback />} />
            <Route element={<NoMatch />} />
          </Routes>
        </AppShell.Main>
      </AppShell>
    </MantineProvider>
  );
};
