module.exports = {
  extends: ['@rustybrooks/eslint-config-prettier'],
  ignorePatterns: ['dist', '.eslintrc.cjs', 'src/vite.config.ts'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: ['./tsconfig.json', './tsconfig.app.json'],
  },
  rules: {
    '@typescript-eslint/no-explicit-any': 'off',
    'no-console': 'off',
    'max-classes-per-file': 'off',
    'import/no-extraneous-dependencies': [
      'error',
      {
        devDependencies: [
          // normally you're not allowed to import devDependencies
          // so make an exception for vite.config.ts
          'vite.config.ts',
        ],
      },
    ],
  },
};
