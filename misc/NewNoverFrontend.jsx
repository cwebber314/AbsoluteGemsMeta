import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Grid, Card, CardContent, Typography } from '@material-ui/core';

function App() {
  const [url, setUrl] = useState("");
  const [imageUrls, setImageUrls] = useState([]);
  const [gifUrls, setGifUrls] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await axios.post('http://localhost:5000/process-video', { url });
    setImageUrls(response.data.image_urls);
    setGifUrls(response.data.gif_urls);
  }

  return (
    <Container maxWidth="md">
      <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
        <TextField
          label="Video URL"
          variant="outlined"
          fullWidth
          value={url}
          onChange={e => setUrl(e.target.value)}
        />
        <Button variant="contained" color="primary" type="submit" style={{ marginTop: '20px' }}>
          Submit
        </Button>
      </form>

      <Grid container spacing={2} style={{ marginTop: '20px' }}>
        {imageUrls.map(url => (
          <Grid item xs={12} sm={6} md={4} key={url}>
            <Card>
              <CardContent>
                <Typography variant="h6">Image</Typography>
                <img src={url} alt="Result" style={{ width: '100%', height: 'auto' }} />
              </CardContent>
            </Card>
          </Grid>
        ))}

        {gifUrls.map(url => (
          <Grid item xs={12} sm={6} md={4} key={url}>
            <Card>
              <CardContent>
                <Typography variant="h6">GIF</Typography>
                <img src={url} alt="Result" style={{ width: '100%', height: 'auto' }} />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default App;


