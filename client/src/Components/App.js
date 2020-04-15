import React from 'react'
import { Container, Button, TextField, Typography, Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  appBar: {
    position: 'relative',
  },
  layout: {
    width: 'auto',
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
    [theme.breakpoints.up(600 + theme.spacing(2) * 2)]: {
      width: 600,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
}));

export default function() {
  const classes = useStyles();
  return (
    <Container>
      <main className={classes.layout}>
        <Grid
          container
          spacing={3}
          direction="column"
          alignItems="center"
        >
          <Grid item>
            <Typography variant="h3" gutterBottom>
              Ordinal
            </Typography>
          </Grid>

          <Grid item>
            <Grid container spacing={1}>
              <Grid item>
                <TextField
                  id="outlined-basic"
                  label="Game ID"
                  variant="outlined"
                  helperText="Enter a four-letter game code"
                />
              </Grid>
              <Grid item>
                <TextField
                  id="outlined-basic"
                  label="Name"
                  variant="outlined"
                  helperText="Let's see what you come up with!"
                />
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Button
              variant="outlined"
              color="primary">
                Join game
            </Button>
          </Grid>
          <Grid item>
            <Button
              variant="outlined"
              color="primary">
                New game
            </Button>
          </Grid>
        </Grid>
      </main>
    </Container>
  )
}