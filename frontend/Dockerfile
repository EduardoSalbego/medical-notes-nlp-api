FROM node:20-alpine

WORKDIR /app

# Copia e instala dependências
COPY package.json .
RUN npm install

# Copia o resto
COPY . .

# Expõe a porta do Vite
EXPOSE 3000

# Roda o servidor de dev
CMD ["npm", "run", "dev", "--", "--host"]