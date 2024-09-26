// import "regenerator-runtime/runtime";

export class Status {
  public status: number;
  public details: string;

  constructor(status: number, details: string) {
    this.status = status;
    this.details = details;
  }
}

class Framework {
  constructor(base_url: string, data: { [x: string]: any }) {
    Object.keys(data)
      .filter(k => {
        return k[0] !== '_';
      })
      .forEach(k => {
        const cmd = data[k];
        const whole_url = `${base_url}/${cmd.simple_url}`;

        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-expect-error
        this[k] = async (context: any) => {
          const headers: Record<string, string> = {};

          const api_key = localStorage.getItem('api-key');
          if (api_key) {
            headers['X-API-KEY'] = api_key;
          }

          let body: string | FormData;
          if (context instanceof FormData) {
            body = context;
            console.log("We've got some form data here", body.getAll('file'), body.getAll('project_key'));
          } else {
            body = JSON.stringify(context);
            headers['Content-Type'] = 'application/json; charset=utf-8';
          }

          // console.log("posting ", JSON.stringify(context), "to", whole_url)
          try {
            const response = await fetch(whole_url, {
              method: 'POST',
              body,
              headers,
              credentials: 'include',
            });

            if (response.status === 500) {
              return new Status(500, 'A server error occurred');
            }
            if (response.status === 400) {
              return new Status(400, await response.json());
            }
            if (response.status === 403) {
              return new Status(403, await response.json());
            }
            if (response.status === 404) {
              return new Status(404, 'Not Found');
            }

            return await response.json();
          } catch (e) {
            console.error(e);
            return new Status(500, 'A server error occurred');
          }
        };
      });
  }
}

export class Frameworks {
  public data: Record<string, Framework>;

  constructor(base_url: string, framework_data: Record<string, any>) {
    this.data = {};

    // console.log(framework_data)
    Object.keys(framework_data)
      .filter(k => {
        return k !== 'user';
      })
      .map(k => {
        this.data[k] = new Framework(base_url, framework_data[k]);
        return true;
      });
  }
}

export const fetchFrameworks = (site: string, prefix: string) => {
  const url = `${site + prefix}/framework/endpoints`;

  const headers: Record<string, string> = {};
  const api_key = localStorage.getItem('api-key');
  if (api_key) {
    headers['X-API-KEY'] = api_key;
  }

  return fetch(url, { headers })
    .then(response => response.json())
    .then(json => {
      return new Frameworks(site, json);
    });
};
