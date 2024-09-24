FROM arm64v8/node:22-alpine AS builder

WORKDIR /srv/src/ui/

COPY package.json yarn.lock /srv/src/ui/
RUN yarn

COPY vite.config.ts tsconfig.json tsconfig.app.json tsconfig.node.json index.html entrypoint.sh postcss.config.cjs .yarnrc.yml /srv/src/ui/
COPY ./src /srv/src/ui/src
COPY ./public /srv/src/ui/public
RUN yarn build


#FROM alpine AS runner
#
#COPY --from=builder /srv/src/ui/dist/ ./srv/src/ui/dist


ENTRYPOINT /srv/src/ui/entrypoint.sh

