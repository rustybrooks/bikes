import { useParams } from 'react-router';
import { Box, Card, Code, Group, LoadingOverlay, NumberFormatter, Stack, Table, Text } from '@mantine/core';
import { DateTime, Duration, Settings } from 'luxon';
import { useActivityRead } from '../api/api-fetch';
import { METER_TO_FOOT, METER_TO_MILE } from '../constants/metrics';

export const Activity = () => {
  const { id: activityId } = useParams();
  const { data: activity, isLoading } = useActivityRead(activityId as unknown as number);

  return (
    <div>
      <LoadingOverlay visible={isLoading} zIndex={1000} overlayProps={{ radius: 'sm', blur: 2 }} />
      {activity && (
        <div>
          <Group>
            <Stack>
              <Card>
                <Text size="sm">
                  {DateTime.fromISO(activity.start_datetime_local).setZone(Settings.defaultZone).toLocaleString(DateTime.DATETIME_MED)}
                </Text>
                <Text size="lg">{activity.activity_name}</Text>
              </Card>
            </Stack>
            <Stack>
              <Card>
                <Group>
                  <Box>
                    <Box>
                      <Text span>
                        <NumberFormatter decimalScale={1} value={activity.distance * METER_TO_MILE} />{' '}
                      </Text>
                      <Text span size="med">
                        mi
                      </Text>
                    </Box>
                    <Text size="sm">Distance</Text>
                  </Box>

                  <Box>
                    <Box>
                      <Text>{Duration.fromObject({ second: activity.moving_time }).toISOTime({ suppressMilliseconds: true })}</Text>
                    </Box>
                    <Text size="sm">Moving Time</Text>
                  </Box>

                  <Box>
                    <Box>
                      <Text span>
                        <NumberFormatter decimalScale={0} value={activity.total_elevation_gain * METER_TO_FOOT} />
                      </Text>{' '}
                      <Text span size="med">
                        ft
                      </Text>
                    </Box>
                    <Text size="sm">Elevation</Text>
                  </Box>

                  <Box>
                    <Text>{activity.suffer_score || 'N/A'}</Text>
                    <Text size="sm">suffer score</Text>
                  </Box>
                </Group>
              </Card>

              <Card>
                <Group>
                  <Box>
                    {activity.weighted_average_watts ? (
                      <Box>
                        <Text span>
                          {' '}
                          <NumberFormatter decimalScale={1} value={activity.weighted_average_watts} />
                        </Text>
                        <Text span size="med">
                          W
                        </Text>
                      </Box>
                    ) : (
                      'N/A'
                    )}

                    <Text size="sm">Weighted Avg Power</Text>
                  </Box>

                  <Box>
                    {activity.kilojoules ? (
                      <Box>
                        <Text span>
                          {' '}
                          <NumberFormatter decimalScale={1} value={activity.kilojoules} />
                        </Text>
                        <Text span size="med">
                          kJ
                        </Text>
                      </Box>
                    ) : (
                      'N/A'
                    )}

                    <Text size="sm">Total Work</Text>
                  </Box>
                </Group>
              </Card>
            </Stack>
          </Group>

          <Table cellPadding="2" cellSpacing="0">
            <Table.Tbody>
              <Table.Tr>
                <Table.Td></Table.Td>
                <Table.Td>Avg</Table.Td>
                <Table.Td>Max</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td>Speed</Table.Td>
                <Table.Td>
                  <NumberFormatter value={(activity.average_speed || 0) * METER_TO_MILE * 3600} decimalScale={1} /> mi/h
                </Table.Td>
                <Table.Td>
                  <NumberFormatter value={(activity.max_speed || 0) * METER_TO_MILE * 3600} decimalScale={1} /> mi/h
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td>Heartrate</Table.Td>
                <Table.Td>
                  {activity.average_heartrate ? (
                    <Text>
                      <NumberFormatter value={activity.average_heartrate || 0} decimalScale={0} /> BPM
                    </Text>
                  ) : (
                    'N/A'
                  )}
                </Table.Td>
                <Table.Td>
                  {activity.max_heartrate ? (
                    <Text>
                      <NumberFormatter value={activity.max_heartrate || 0} decimalScale={0} /> BPM
                    </Text>
                  ) : (
                    'N/A'
                  )}
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td>Cadence</Table.Td>
                <Table.Td>{activity.average_cadence ? <Text>{activity.average_cadence} RPM</Text> : 'N/A'}</Table.Td>
                <Table.Td></Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td>Power</Table.Td>
                <Table.Td>
                  {activity.average_watts ? (
                    <Text>
                      <NumberFormatter value={activity.average_watts} decimalScale={0} /> W
                    </Text>
                  ) : (
                    'N/A'
                  )}
                </Table.Td>
                <Table.Td>
                  {activity.max_watts ? (
                    <Text>
                      <NumberFormatter value={activity.max_watts} decimalScale={0} /> W
                    </Text>
                  ) : (
                    'N/A'
                  )}
                </Table.Td>
              </Table.Tr>
            </Table.Tbody>{' '}
          </Table>

          <Code block>{JSON.stringify(activity, null, 2)}</Code>
        </div>
      )}
    </div>
  );
};
