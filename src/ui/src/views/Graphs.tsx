import { Tabs } from '@mantine/core';
import { Progress } from './graphs/Progress';

export const Graphs = () => {
  return (
    <Tabs defaultValue="progress">
      <Tabs.List>
        <Tabs.Tab value="progess">Progress</Tabs.Tab>
      </Tabs.List>

      <Tabs.Panel value="progress">
        <Progress />
      </Tabs.Panel>
    </Tabs>
  );
};
